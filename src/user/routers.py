from typing import Union

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException, UploadFile, status, File

from . import schemas, models
from database import get_session
from .utils import create_user_db, converter_file, get_authenticate_user


router = APIRouter(prefix="/user",
                   tags=["User"])


@router.post("/add", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
async def create_user(user: schemas.UserIn,
                      session: AsyncSession = Depends(get_session)) -> models.User:
    """ Создание пользователя, POST:
           1.	Принимает на вход запросы с именем пользователя;
           2.	Создаёт в базе данных пользователя заданным именем,
               так же генерирует уникальный идентификатор пользователя и UUID токен доступа
               (в виде строки) для данного пользователя;
           3.	Возвращает сгенерированные идентификатор пользователя и токен.
    :param user: user
    :param session: session
    :return: models.User
    """
    return await create_user_db(user, session)


@router.post("/upload_file/", status_code=status.HTTP_200_OK)
async def upload_file(
        user_id: str,
        token: str,
        file: UploadFile,
        session: AsyncSession = Depends(get_session)
        ):
    """
    1.	Принимает на вход запросы, содержащие уникальный идентификатор пользователя,
        токен доступа и аудиозапись в формате wav;
    2.	Преобразует аудиозапись в формат mp3, генерирует для неё уникальный UUID идентификатор и
        сохраняет их в базе данных;
    3.	Возвращает URL для скачивания записи вида
        http://host:port/record?id=id_записи&user=id_пользователя."""
    user: Union[models.User, None] = await get_authenticate_user(token, user_id, session)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or token",
        )

    if file.content_type == "audio/x-wav":
        url_upload = await converter_file(file, session, user)
        return {"filename": file.filename,
                "url": url_upload
                }
    else:
        raise TypeError("Tолько файлы типа wav")




