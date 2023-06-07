import uuid

from typing import Dict

from sqlalchemy import Boolean, ForeignKey, String
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID

from database import Base

    
class Record(Base):
    __tablename__ = 'record'
    
    record_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    id_user: Mapped[UUID] = mapped_column(ForeignKey("user.user_id"))

    user = relationship("User", back_populates="records")



class User(Base):
    __tablename__ = 'user'
    
    user_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    token: Mapped[str] = mapped_column(String())

    
    records = relationship("Record", back_populates="user")

    def to_json(self) -> Dict:
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
