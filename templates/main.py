import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from starlette.requests import Request
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates
from fastapi import Form
from fastapi.responses import RedirectResponse

books = [
    {"id": 1, "name": "Metro 2033", "author": "Дмитро Глуховський", "price": "100"},
]

DATABASE_URL = "sqlite:///./test1.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False}, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
import os
templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), "templates"))

class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    author = Column(String, index=True)
    price = Column(String, index=True)

Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

from pydantic import BaseModel

class BookCreate(BaseModel):
    name: str
    author: str
    price: str

@app.get("/book/")
def read_books(db: Session = Depends(get_db)):
    return db.query(Book).all()

@app.post("/book_create/")
def create_book(name: str = Form(...), author: str = Form(...), price: str = Form(...), db: Session = Depends(get_db)):
    db_book = Book(name=name, author=author, price=price)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return RedirectResponse(url="/book_html/", status_code=303)

@app.post("/book_delete/")
def delete_book(book_id: int = Form(...), db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(book)
    db.commit()
    return RedirectResponse(url="/book_html/", status_code=303)

@app.get("/book_html/")
def read_books_html(request: Request, db: Session = Depends(get_db)):
    books = db.query(Book).all()
    return templates.TemplateResponse(
        "book.html",
        {
            "request": request,
            "books": books,
            "data": {"message": "Books loaded"},
        },
    )

@app.post("/book_update/")
def update_book(book_id: int = Form(...), name: str = Form(...), author: str = Form(...), price: str = Form(...), db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    book.name = name
    book.author = author
    book.price = price
    db.commit()
    db.refresh(book)
    return RedirectResponse(url="/book_html/", status_code=303)

uvicorn.run(app)
