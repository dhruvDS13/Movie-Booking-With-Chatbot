from fastapi import APIRouter
from services.tmdb_service import get_trending_movies

router = APIRouter(prefix="/movies", tags=["movies"])


@router.get("")
def get_movies():
    return get_trending_movies()