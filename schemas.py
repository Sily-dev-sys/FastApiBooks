from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=50, description="Ім'я користувача")
    email: str
    city: str = Field(..., min_length=2, description="Місто користувача")

# Модель для відповіді з ID
class User(UserCreate):
    id: int