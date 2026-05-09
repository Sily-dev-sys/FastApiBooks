from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
books = [
    {"id": 1, "name": "Metro 2033", "author": "Дмитро Глуховський", "price": "100"},
]

DATABASE_URL = "sqlite.///./test1.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    author = Column(String)
    price = Column(String)

Base.metadata.create_all(bind=engine)
