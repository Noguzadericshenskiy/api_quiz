import aiohttp
from datetime import datetime
from aiohttp import ContentTypeError
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from . import models, schemas

from config import URL_GET_QUIZ_QUESTIONS


async def getting_quiz_questions(session: AsyncSession, num: int) -> list[models.Question]:
    """Получение запросов для викторины"""
    fails: int = num
    while fails > 0:
        questions: list[schemas.QuestionIn] = await request_questions(num)
        fails: int = await add_questions_in_db(session, questions)

    questions_list = await get_question_in_db(num, session)

    return questions_list
            

async def request_questions(num) -> list[schemas.QuestionIn]:
    """Получение списка вопросов от API"""
    timeout = aiohttp.ClientTimeout(total=60)
    url = URL_GET_QUIZ_QUESTIONS + str(num)
    try:
        async with aiohttp.ClientSession() as conn:
            async with conn.get(url, timeout=timeout) as response:
                if response.status == 200:
                    json_data = await response.json()
                    list_obj_question = [schemas.QuestionIn(**question) for question in json_data]
                    return list_obj_question
                
                else:
                    raise ContentTypeError(f"Ошибка при получении ответа от API Type Error")
    except Exception as err:
        logger.error(err)
        raise err


async def add_questions_in_db(
    session: AsyncSession, 
    questions: list[schemas.QuestionIn]
) -> int:
    """Добавление данных в БД"""
    fail_count: int = 0
    
    for question in questions:
        question_db = creating_an_object(question)
        if not await check_question(session, question_db):
            await add_db(question_db, session)
        else:
            fail_count += 1
    
    return fail_count


def creating_an_object(schemas_in: schemas.QuestionIn) -> models.Question:
    question = models.Question()
    question.question_id = schemas_in.question_id
    question.question = schemas_in.question
    question.answer = schemas_in.answer
    question.created_at = datetime.fromisoformat(schemas_in.created_at[:-1]).astimezone(tz=None)
    return question

        
async def check_question(session: AsyncSession, question: schemas.QuestionIn):
    """Проверка на уникальность вопроса"""
    request = select(models.Question).where(models.Question.question == question.question)
    async with session.begin():
        result = await session.execute(request)
        return result.fetchall()


async def add_db(data: models.Question, session: AsyncSession):
    """Добавление вопроса в БД"""
    async with session.begin():
        session.add(data)
        await session.commit()


async def get_question_in_db(num: int, session: AsyncSession) -> list[models.Question]:
    """Получение нескольких последних вопросов из БД"""
    request = select(models.Question).order_by(models.Question.id.desc()).limit(num)
    async with session.begin():
        result = await session.execute(request)
    return result.scalars().all()[::-1]
