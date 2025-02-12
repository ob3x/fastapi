from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

DB_URL = "postgresql://postgres:password@localhost:5432/users"

engine = create_engine(DB_URL)
LocalSession = sessionmaker(autocommit = False, autoflush = False, bind = engine)

Session = LocalSession()

Base = declarative_base()

def get_db():
    db = LocalSession()
    try:
        yield db
    finally:
        db.close()


def create_table():
    Base.metadata.create_all(bind = engine)


class Users(Base):
    __tablename__ = "Users"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)

user1 = Users(name = "x", age = 1)

Session.add(user1)

Session.commit()
Session.refresh(user1)

Session.close()