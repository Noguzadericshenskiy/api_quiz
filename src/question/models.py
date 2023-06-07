from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column

from sqlalchemy.dialects.postgresql import TIMESTAMP

from database import Base


class Question(Base):
    __tablename__ = 'question'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    question_id: Mapped[int] = mapped_column(Integer)
    question: Mapped[str] = mapped_column(String(250))
    answer: Mapped[str] = mapped_column(String(100))
    created_at: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP(timezone=True))
