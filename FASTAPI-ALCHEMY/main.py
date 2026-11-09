from sqlalchemy import create_engine,Column, String, Integer, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from fastapi import FastAPI, Depends, HTTPException
from typing import Optional
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

# @app.get("/")
# def home(db: Session = Depends(check_db)):
#     return {
#         "message":"DB Connected",
#     }

@app.post("/todo")
def create_todo(title: str,db: Session = Depends(check_db)):
    todo = Todo(
        title = title,
        Completed = False
    )
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return{
        "message":"Todo Created",
        "Data":todo
    }


#read total data
@app.get("/todo")
def read_todo(db: Session = Depends(check_db)):
    todo = db.query(Todo).all()

    return{
        "Total":len(todo),
        "Data":todo
    }



#to get a specific data
@app.get("/todo/{todo_id}")
def get_data(todo_id: int,db: Session = (Depends(check_db))):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()

    if not todo:
        raise HTTPException(status_code=404,detail="Todo not found")
    return {
        "Data":todo
    }

@app.put("/todo/{todo_id}")
def update_data(todo_id :int, todo_title : str, db: Session = Depends(check_db)):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()

    if not todo:
        raise HTTPException(status_code=404,detail="Todo not found")

    todo.title = todo_title
    db.commit()
    db.refresh(todo)

    return {
        "Data":todo
    }


@app.patch("/todo/{todo_id}")
def todo_patch(todo_id:int, title: Optional[str] = None,Completed: Optional[bool] = None ,db: Session = Depends(check_db)):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404,detail="The TODO not found")
    if title is not None:
            todo.title = title
    if Completed is not None:
            todo.Completed = Completed

    db.commit()
    db.refresh(todo)


    return {
        "Data":todo
    }





    
