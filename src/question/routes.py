import datetime

from typing import Union
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_session
from question import models, schemas
from .utils import getting_quiz_questions


router = APIRouter(prefix="/question",
                   tags=["Question"])



@router.post('/', status_code=201, response_model=list[schemas.QuestionOut])
async def add_questions(questions_num: int, db: AsyncSession = Depends(get_session)) -> list[models.Question]:
    """
    1. В сервисе реализован POST REST метод, принимающий на вход запросы с
       содержимым вида {"questions_num": integer}.
    2. После получения запроса сервис, запрашивает с публичного API
       (англоязычные вопросы для викторин) https://jservice.io/api/random?count=1 указанное
       в полученном запросе количество вопросов.
    3. Далее, полученные ответы сохраняются в базе данных из п. 1б а именно, следующая информация:
        1. ID вопроса,
        2. Текст вопроса,
        3. Текст ответа,
        4. Дата создания вопроса.

        В случае, если в БД имеется такой же вопрос, к публичному API с викторинами
        выполняются дополнительные запросы, до тех пор, пока не будет получен уникальный
        вопрос для викторины.
    4. Ответ на запрос сервис возвращает список последних добавленных вопросов.
"""
    return await getting_quiz_questions(db, questions_num)
