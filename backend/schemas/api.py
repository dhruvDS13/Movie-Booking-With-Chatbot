from pydantic import BaseModel, Field
from typing import Optional


class ChatRequest(BaseModel):
    user_id: str = Field(default="demo-user")
    message: str


class ChatResponse(BaseModel):
    reply: str


class BookingRequest(BaseModel):
    user_id: str = Field(default="demo-user")
    show_id: int
    seat_numbers: list[str]


class BookingResponse(BaseModel):
    booking_id: str
    show_id: int
    user_id: str
    seat_numbers: list[str]
    total_amount: int
    status: str


class MovieQuery(BaseModel):
    genre: Optional[str] = None
    q: Optional[str] = None
    limit: int = 12
