from fastapi import (
    HTTPException,
    status
)

class UnauthError(HTTPException):
    """ Некоректные имя пользователя или пароль """

    def __init__(self) -> None:
        super().__init__(status.HTTP_401_UNAUTHORIZED, detail='Некоректные имя пользователя или пароль', headers={'WWW-Authenticate': 'Bearer'})

class UsernameError(HTTPException):
    """ Пользователь с таким логином уже существует """

    def __init__(self) -> None:
        super().__init__(status.HTTP_409_CONFLICT, detail='Пользователь с таким логином уже существует')

class DoesNotNoteError(HTTPException):
    """ Такой записи не существует """

    def __init__(self) -> None:
        super().__init__(status.HTTP_409_CONFLICT, detail='Такой записи не существует')