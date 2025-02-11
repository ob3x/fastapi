from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

from fastapi import FastAPI, Depends
from pydantic import BaseModel
import uvicorn

app = FastAPI()

DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread" : False})

SessionLokal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLokal()
    try:
        yield db
    finally:
        db.close()

class UserCreate(BaseModel):
    name : str
    email : str

class UserResponse(BaseModel):
    id : int
    name : str
    email : str

    class Config:
        orm_mode = True    


@app.post("/users/", response_model=UserResponse)
def create_user(user : UserCreate, db:Session=Depends(get_db)):
    db_user = User(name = user.name, email = user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

if __name__ == "__main__":
    uvicorn.run(app)