from fastapi import APIRouter
from models.note import Note
from config.db import conn
from fastapi.responses import HTMLResponse
from fastapi import FastAPI, Request
from schemas.note import noteEntity,notesEntity
from fastapi.templating import Jinja2Templates
note = APIRouter()
templates = Jinja2Templates(directory="templates")
# note.include_router(note)


@note.get("/",response_class=HTMLResponse)
async def read_item(request: Request):
    # docs = conn.notes.notes.find_one({})
    # print(docs)
    newDocs = []
    docs = conn.notes.notes.find({})
    for doc in docs:
        # print(doc)
        newDocs.append({
            "id": doc["_id"],
            "title": doc["title"],
            "desc": doc["desc"],
            "important": doc["important"]
    
        })
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"newDocs": newDocs}
    )

@note.post("/")
async def create_item(request: Request):  
    form = await request.form()
    # print(form)
    formDict = dict(form)
    formDict["important"] = True if formDict.get("important") == "on" else False
    note = conn.notes.notes.insert_one(formDict)
    return {"Success": True}

#implement the put and delete like the note.put and note.delete yesss!!.

@note.put("/")
async def update_item(request: Request):
    pass


@note.delete("/")
async def delete_item(request:Request):
    pass