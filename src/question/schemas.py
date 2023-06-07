from pydantic import BaseModel, Field


class QuestionBase(BaseModel):
    question: str = Field(str)
    question_id: int = Field(int, alias="id")
    answer: str = Field(str)
    created_at: str = Field(str)


class QuestionIn(QuestionBase):
    ...


class QuestionOut(BaseModel):
    id: int
    question_id: int
    question: str
    answer: str

    class Config:
        orm_mode = True
