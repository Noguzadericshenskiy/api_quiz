from pydantic import BaseModel, Field, UUID4



class UserBase(BaseModel):
    name: str = Field(title="Name",
                      description="Name of the user", 
                      min_length=4)
 
    
class UserIn(UserBase):
    ...

    
class UserOut(BaseModel):
    user_id: UUID4
    name: str
    token: str

    class Config:
        orm_mode = True

    
class RecordBase(BaseModel):
    record_id: UUID4
    id_user: UserBase


class RecordIn(RecordBase):
    ...


class RecordOut(BaseModel):
    ...


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    name: str | None = None
