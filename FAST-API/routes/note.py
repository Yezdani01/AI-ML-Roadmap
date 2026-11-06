from fastapi import APIRouter
from models.note import Note
from config.db import conn
from fastapi import Form
from fastapi.responses import HTMLResponse
from fastapi import FastAPI, Request
from schemas.note import noteEntity,notesEntity
from fastapi.templating import Jinja2Templates
from bson import ObjectId
note = APIRouter()
templates = Jinja2Templates(directory="templates")
# note.include_router(note)


@note.get("/",response_class=HTMLResponse) #find use karte
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

@note.post("/") #insert_one use karte 
async def create_item(request: Request):  
    form = await request.form()
    # print(form)
    formDict = dict(form)
    formDict["important"] = True if formDict.get("important") == "on" else False
    note = conn.notes.notes.insert_one(formDict)
    return {"Success": True}

#implement the put and delete like the note.put and note.delete yesss!!.

@note.put("/{id}") #update_one use karte 
async def update_item(id : str,title: str = Form(...),
    desc: str = Form(...),
    important: bool = Form(False)):
    #we have the id from the mongodb and through that we know which note to update. 
    # form = await request.form()
    # formDict = dict(form)
    formDict = {
    "title": title,
    "desc": desc,
    "important": important
}

    # formDict["important"] = True if formDict.get("important") == "on" else False

    result = conn.notes.notes.update_one(
    {"_id": ObjectId(id)},
    {"$set": formDict}
)

    if result.matched_count == 0:
        return {"Error": "Note not found"}

    return {"Success": True}


@note.delete("/{id}") #delete_one use karte.
async def delete_item(id : str):
    result = conn.notes.notes.delete_one(
        {"_id": ObjectId(id)}
    )

    if result.deleted_count == 0:
        return {"Error": "Note not found"}
    
    return {"Success": True}