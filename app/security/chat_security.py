# from fastapi import WebSocket, Depends, Query
# from fastapi.responses import HTMLResponse
# from fastapi_jwt_auth import AuthJWT
# from fastapi_jwt_auth.exceptions import AuthJWTException
# from pydantic import BaseModel
#
# from app.config import load_config
#
# config = load_config()
#
# class Settings(BaseModel):
#     authjwt_secret_key: str = config.secret_key
#     authjwt_token_location: set = {"cookies"}
#
# @AuthJWT.load_config
# def get_config():
#     return Settings()


