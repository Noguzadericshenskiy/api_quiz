from __future__ import annotations
import os

from datetime import datetime, timedelta
import aiofiles
from starlette.datastructures import UploadFile
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status
from pydub import AudioSegment

from . import schemas, models
from config import CURRENT_PATH, HOST, PORT, SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES


async def get_user_by_name(name, db) -> models.User:
    request = select(models.User).where(models.User.name == name)
    async with db.begin():
        user = await db.execute(request)
    return user.scalars().one()


async def get_authenticate_user(token, user_id, session: AsyncSession) -> models.User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("name")
        user: models.User = await get_user_by_name(username, session)
        if str(user.user_id) != user_id:
            raise credentials_exception
        return user
    except JWTError:
        raise credentials_exception


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def create_user_db(user: schemas.UserBase, db: AsyncSession) -> models.User:
    "Создает пользователя в БД"
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    new_user: models.User = models.User(**user.dict())
    new_user.token = create_access_token(new_user.to_json(), expires_delta=access_token_expires)

    async with db.begin():
        db.add(new_user)
    return new_user


async def converter_file(uploaded_file: UploadFile, db: AsyncSession, user: models.User) -> str:
    path_wav_fail = await create_upload_file(uploaded_file)
    path_mp3_fail = converter(path_wav_fail)
    delete_file(path_wav_fail)
    url_record = await write_info_to_db(path_mp3_fail, user_id=str(user.user_id), db=db)

    return url_record


async def create_upload_file(uploaded_file):
    path_wav_fail = os.path.join(CURRENT_PATH, "sound", uploaded_file.filename)

    async with aiofiles.open(path_wav_fail, 'wb') as out_file:
        content = await uploaded_file.read(1024)
        await out_file.write(content)
    return path_wav_fail


def converter(uploaded_path: str) -> str:
    path_save = os.path.join(CURRENT_PATH, "sound", "simple_mp3.mp3")
    # AudioSegment.from_mp3(uploaded_path).export(path_save, format="wav")
    AudioSegment.from_wav(uploaded_path).export(path_save, format="mp3")
    return path_save


def delete_file(path_waw_file: str) -> None:
    if os.path.exists(path_waw_file):
        os.remove(path_waw_file)
    else:
        raise FileExistsError("File not create")


async def write_info_to_db(path_to_the_file: str, user_id: str, db: AsyncSession):
    async with db.begin():
        new_record: models.Record = models.Record(id_user=user_id)
        db.add(new_record)
        await db.flush()
        id_record = new_record.record_id
        rename_file(path_to_the_file, str(id_record)+".mp3")
        url = f"http://{HOST}:{PORT}/record?id={id_record}&user_id={user_id}"
    return url


def rename_file(old_name, new_name) -> None:
    path_details = os.path.split(old_name)[0]
    new_path = os.path.join(path_details, new_name)
    os.rename(old_name, new_path)

