import os
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse


from config import CURRENT_PATH

router = APIRouter(prefix="/record",
                   tags=["Record"])


@router.get("/", response_class=FileResponse)
async def send_file(id: str, user_id: str):
    """1.	Предоставляет возможность скачать аудиозапись по ссылке"""
    return os.path.join(CURRENT_PATH, "sound", id + ".mp3")
