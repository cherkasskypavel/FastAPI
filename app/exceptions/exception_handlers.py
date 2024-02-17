from fastapi import Request
from fastapi.responses import JSONResponse

from app.main import app
import app.exceptions.custom_exceptions as ce

@app.exception_handler(ce.UserNotFoundException)
def custom_exception_a_handler(request: Request, exception: ce.UserNotFoundException):
    return JSONResponse(
        status_code=exception.status_code,
        content={'error': exception.detail}
    )


@app.exception_handler(ce.UserAlreadyExistsException)
def custom_exception_a_handler(request: Request, exception: ce.UserAlreadyExistsException):
    return JSONResponse(
        status_code=exception.status_code,
        content={'error': exception.detail}
    )


@app.exception_handler(ce.PostNotFoundException)
def custom_exception_a_handler(request: Request, exception: ce.PostNotFoundException):
    return JSONResponse(
        status_code=exception.status_code,
        content={'error': exception.detail}
    )


##  Возможно, не работает из-за конфликтов с @field_validator
# @app.exception_handler(ValueError)
# def value_error_handler(request: Request, exception: ValidationError):
#     return  JSONResponse(
#         status_code=status.HTTP_400_BAD_REQUEST,
#         content={'error': str(exception)}
#     )
