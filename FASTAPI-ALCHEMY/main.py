from sqlalchemy import create_engine,Column, String, Integer, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from fastapi import FastAPI, Depends
app = FastAPI()
DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    DATABASE_URL,
    connect_args = {"check_same_thread":False}
)

sessionlocal = sessionmaker(bind=engine)

Base = declarative_base()

class Todo(Base):
    __tablename__ = "The_Todo"

    id = Column(Integer,primary_key=True,index=True)
    title = Column(String)
    Completed = Column(Boolean)


Base.metadata.create_all(bind=engine)

def check_db():
    db = sessionlocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def home(db: Session = Depends(check_db)):
    return {
        "message":"DB Connected"
    }
