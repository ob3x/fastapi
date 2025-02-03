from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()
books = []
book_id = 1

class Book(BaseModel):
    id : int
    title : str
    author : str
    genre : str
    rating : float
    status : bool

@app.get("/book-list/")
def book_list():
    return {"Lista książek" : books}


@app.post("/add-book/")
def add_book(book : Book):
    global book_id
    book.id = book_id
    books.append(book)
    book_id += 1
    return {"Dodano" : book}

@app.get("/recomended-books/")
def recomended_books(rating : float):
    filtred_books = [book for book in books if book.rating >= rating]
    return {f"Books with rating under {rating} stars" : filtred_books}

@app.put("/borrow-book/")
def borrow_book(id : int):
    if id <= 0:
        return {"Error" : "Wrong ID"}
    
    for book in books:
        if book.id == id:
            if not book.status:
                return {"Error" : "Book is not available"}
            book.status = False
            return {"message" : "You borrowed successfully", "book" : book}
            
    return {"Error" : "Book not found"}

@app.put("/return-book/")
def return_book(id : int):
    if id <= 0:
        return {"Error" : "Wrong ID"}
     
    for book in books:
        if book.id == id:
            if not book.status:
                book.status = True
                return {"message" : "Book successfully returned", "book" : book}

    return {"Error" : "Book is either not borrowed or not found"}


@app.get("/borrow-history/")
def borrow_history():
    borrowed_books = [book for book in books if not book.status]

    return {"List of borrowed books" : borrowed_books}
