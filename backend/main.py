from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import os
from dotenv import load_dotenv

from routers import bookings, chat, movies, shows


env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

app = FastAPI(title="BookMyMovie AI", version="1.0.0")

origins = [
    "https://movie-booking-with-chatbot.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins or ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router)
app.include_router(movies.router)
app.include_router(shows.router)
app.include_router(bookings.router)

frontend_dir = Path(__file__).resolve().parent.parent / "frontend"
if frontend_dir.exists():
    app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="frontend")
@app.get("/health")
def health():
    return {"status": "ok"}