from db import SessionLocal, User

db = SessionLocal()

print(db.query(User).all())

db_user = User(name="Test", email="test@example.com", city="Test City")