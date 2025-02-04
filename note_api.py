from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime

app = FastAPI()

subjects = ["math", "chemistry", "pe", "it", "physics", "geography"]
elements = [element.lower() for element in subjects]
notes = []

note_id = 1

class Notes(BaseModel):
    id : int
    title : str
    subject : str
    date : str
    text : str


@app.get("/notes/")
def check_notes():
    return {"Notes" : notes}

@app.get("/subjects/{subject_id}")
def read_subject(subject_id : str):
    if subject_id not in elements:
        raise HTTPException(status_code=404, detail="Subject not found")

    local_notes = [note for note in notes if note.subject == subject_id]

    if not local_notes:
        raise HTTPException(status_code=404, detail="No notes found for this subject")

    return {"Notes": local_notes}


@app.post("/add-notes/")
def add_notes(note : Notes):
    global note_id
    current_time = datetime.now().strftime("%H:%M:%S")

    note.id = note_id
    note.date = current_time
    if note.subject not in subjects:
        raise HTTPException(status_code=400, detail="Wrong subject")

    notes.append(note)
    note_id += 1    
    return {"Note" : note}



@app.delete("/notes-delete/")
def delete_notes(note_id : int):
    for note in notes:
        if note.id == note_id:
            notes.remove(note)
            return {"message": "Note successfully deleted", "note": note}

    raise HTTPException(status_code=404, detail="Note not found")