from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()
books = []

class Book(BaseModel):
    title : str
    author : str
    genre : str
    rating : float

@app.get("/book-list/")
def book_list():
    return {"Lista książek" : books}


@app.post("/add-book/")
def add_book(book : Book):
    books.append(book)
    return {"Dodano" : book}

@app.get("/recomended-books")
def recomended_books(rating : float):
    book = [book for book in books if book.rating >= rating]
    return book
