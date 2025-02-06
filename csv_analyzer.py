from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
import re

app = FastAPI()

def file_basic(file_name):
    try:
        with open(f"{file_name}.csv", "r", encoding="utf-8") as file: 
            return file.read()
        
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/read-csv/{file_name}")
def read_csv(file_name : str):
    file = file_basic(file_name)
    return {"File" : file}

@app.get("/count-words/{file_name}")
def words_count(file_name : str):
    file = file_basic(file_name)
    words = file.split()
    return {"words_count" : len(words)}

@app.get("/count-letters/{file_name}")
def letters_count(file_name : str):
    file = file_basic(file_name)
    letters = re.sub(r"[^a-zA-Z]", "", file)
    return {"letter_count": len(letters)}

@app.get("/count-lines/{file_name}")
def lines_count(file_name : str):
    file = file_basic(file_name)
    lines = file.splitlines()
    return {"lines_count": len(lines)}

@app.get("/count-everyword/{file_name}")
def count_everyword(file_name : str):
    file = file_basic(file_name)
    words = file.split()
    words_count = []
    for word in words:
        word_length = len(word)
        words_count.append({word_length : word})

    return {"Lenght of every word" : words_count}

@app.get("/download/{file_name}")
def download_file(file_name : str):
    file_path = f"{file_name}.csv"
    return FileResponse(file_path, media_type='text/csv', filename=f"{file_name}.csv")
