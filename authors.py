import itertools
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from collections import defaultdict

app = FastAPI()


books_db = defaultdict(list)


class Author(BaseModel):
    name: str
    author_id: int


class Book(BaseModel):
    title: str
    book_id: int
    author: Author


@app.post("/books")
def create_book(book: Book):
    books_db[book.author.author_id].append(book.dict())
    return book


@app.get("/database")
def get_the_entire_database():
    return books_db


# Authors perspective

@app.get("/authors/{author_id}")
def get_author_info_by_author_id(author_id:int):
    for books in books_db.values():
        for book in books:
            if book["author"]["author_id"] == author_id:
                return book["author"]
    raise HTTPException(status_code=404,detail="no teacher")






@app.get("/authors/{author_id}/books")
def get_books_by_author_id(author_id: int):
    books_list = []
    for book in itertools.chain(*books_db.values()):
        if book["author"]["author_id"] == author_id:
            book_copy = book.copy()  
            del book_copy["author"]  
            books_list.append(book_copy)

    if not books_list:
        raise HTTPException(status_code=404, detail=f"No books found for author_id {author_id}")

    return {"books": books_list}

    


@app.get("/authors")
def get_all_authors():
    authors = []
    for books in books_db.values():
        for book in books:
            author = book["author"]
            if author not in authors:
                authors.append(author)
    return {"authors": authors}






@app.put("/authors/{author_id}")
def update_author_info(author_id:int, new_author:Author):
    for book in itertools.chain(*books_db.values()):
        if book["author"]["author_id"] == author_id:
            book["author"] = new_author.dict()
            return book
    raise HTTPException(status_code=404,detail="no teacher")





# books perspective

@app.get("/books")
def get_all_books():
    books_list = []
    for books in books_db.values():
        for book in books:
            del book["author"]["author_id"]
            books_list.append(book)
    return books_list




@app.get("/books/{book_id}")
def get_book_by_id(book_id:int):
    for book in itertools.chain(*books_db.values()):
        if book["book_id"] == book_id:
            return book
    raise HTTPException(status_code=404,detail="no book")




@app.get("/books/{book_id}/authors")
def get_books_by_author(book_id:int):
    authors_list = []
    for book in itertools.chain(*books_db.values()):
        if book["book_id"] == book_id:
            authors = book["author"]
            authors_list.append(authors)

    if not authors_list:
        raise HTTPException(status_code=404,detail="no book")
    return {"authors":authors_list}




@app.put("/books/{book_id}")
def update_book_info(book_id:int, new_book:Book):
    for book in itertools.chain(*books_db.values()):
        if book["book_id"] == book_id:
            book = new_book.dict()
            return book
        
    raise HTTPException(status_code=404,detail="no book")
