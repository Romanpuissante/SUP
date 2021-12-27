from fastapi import (
    HTTPException,
    status
)

unauthError = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Некоректные имя пользователя или пароль',
    headers={'WWW-Authenticate': 'Bearer'},
)

usernameError = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Пользователь с таким логином уже существует"
)

doesNotNoteError = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Такой записи не существует",
)



    