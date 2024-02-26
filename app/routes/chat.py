from datetime import datetime

from fastapi import Depends, Request, Response
from fastapi import HTTPException, status
from fastapi.responses import HTMLResponse
from fastapi.routing import APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from fastapi.websockets import WebSocket
from fastapi.websockets import WebSocketDisconnect

import app.db.schemas as sc
import app.security.security as sec
import app.db.crud as crud
import app.security.chat_security as cs

templates = Jinja2Templates('templates')

TIME_FORMAT = '%H:%M'
GREETING = 'Welcome, {}!'
CONNECTED_USERS = {}
CHAT_HISTORY = []

chat = APIRouter(prefix='/chat')


async def load_chat_history(websocket: WebSocket):
    for msg in CHAT_HISTORY:
        await websocket.send_text('{} {}: {}'.format(*msg))


@chat.post('/login')
async def auth_chat(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await crud.get_user_by_email(form_data.username)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Пользователь {form_data.username} не найден.')
    else:
        token = await sec.authenticate_user(user, form_data.password)
        response = Response(status_code=200)
        response.set_cookie(key='access_token', value=token)
        return response


@chat.websocket('/start_chat')
async def connect_to_chat(web_socket: WebSocket,
                          chat_token: str):

    await web_socket.accept()

    try:
        user = await sec.get_user_from_token(chat_token)
    except HTTPException as e:
        await web_socket.send_text(f'Ошибка аутентификации: {e}')
        await web_socket.close()
        return

    CONNECTED_USERS.update(
        {web_socket: {'user_id': user.id}}
    )

    username = user.email.split('@')[0]

    await web_socket.send_text(GREETING.format(username))
    await load_chat_history(web_socket)

    while True:
        try:
            msg_text = await web_socket.receive_text()
            msg_time = datetime.now().strftime(__format=TIME_FORMAT)
            new_msg = (msg_time, username, msg_text)
            CHAT_HISTORY.append(new_msg)
            for online_user in CONNECTED_USERS.keys():
                await online_user.send_text('{} {}: {}'.format(*new_msg))

        except WebSocketDisconnect:
            del CONNECTED_USERS[web_socket]
            break

@chat.get('/', response_class=HTMLResponse)
async def get_chat_page(request: Request):

    token = request.cookies.get('access_token')
    if token is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Для чата необходимо авторизироваться!')

    user: sc.UserFromToken = await sec.get_user_from_token(token)
    username = user.email.split('@')[0]

    return templates.TemplateResponse(
        request=request,
        name='chat.html',
        context={"username": username}
    )

