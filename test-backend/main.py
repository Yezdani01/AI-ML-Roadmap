from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
app = FastAPI()

class employee(BaseModel):
    id: int
    name: str
    age: int
    salary: int
    email: str

class update_emp(BaseModel):
    salary: Optional[int]
    email: Optional[str]

employees = []

@app.get("/")
def read():
    return {
        "message":"This is the message"
    }

@app.post("/")
def create(id: int,name:str,age:int,salary:int,email:Optional[str]):
    data = {
        "id":id,
        "name":name,
        "age":age,
        "salary":salary,
        "email":email
    }
    employees.append(data)
    return {
        "message":"Post done",
        "data":employees
    }

@app.get("/employees")
def print_employees():
    data = [i for i in employees]
    return {
        "message":"These are the employees",
        "Data":data
    }


@app.get("/employees/{employee_id}")
def get_employee(employee_id:int):
    for i in employees:
        if i["id"] == employee_id:
            data = i
            return{
                "Data":data
            }    


class update_emp(BaseModel):
    salary: Optional[int]
    email: Optional[str]

@app.patch("/employees_update/{employee_id}")
def update_employee(employee_id:int,update_emp:update_emp):
    for i in employees:
        if i["id"] == employee_id:
            if update_emp.salary == i["salary"]:
                continue
            else:
                i["salary"] = update_emp.salary
            if update_emp.email == i["email"]:
                continue
            else:
                i["email"] = update_emp.email
    return{
        "message":f"the {employee_id}'s data is updated",
        "Data":i
            } 
        
    

