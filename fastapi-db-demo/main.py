from fastapi import FastAPI,Depends,HTTPException
from typing import Optional
from sqlalchemy import create_engine,Column,String,Integer
from sqlalchemy.orm import Session,sessionmaker,declarative_base

app = FastAPI()

DATABASE_URL = "sqlite:///./test.db"


engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

session_local = sessionmaker(bind=engine)

Base = declarative_base()

class Person(Base):
    __tablename__ = "The People"
    id = Column(Integer,primary_key=True,index=True)
    name = Column(String)
    gender = Column(String)


Base.metadata.create_all(bind=engine)

def check_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def get_demo(db: Session = Depends(check_db)):

    return {"message":"here we are"}


@app.post("/person")
def create_person(name: str, gender: str,db: Session = Depends(check_db)):
    person = Person(
        name = name,
        gender = gender
    )

    db.add(person)
    db.commit()
    db.refresh(person)
    return {
        "message":"Person Created",
        "Data":person
    }

