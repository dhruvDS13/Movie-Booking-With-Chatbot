from fastapi import APIRouter, Query
from services.tmdb_service import get_trending_movies

router = APIRouter(prefix="/movies", tags=["movies"])


@router.get("")
def get_movies(
    genre: str | None = None,
    q: str | None = None,
    limit: int = Query(default=12, ge=1, le=30),
):
    movies = get_trending_movies()

    # genre filter
    if genre:
        movies = [
            movie for movie in movies
            if genre.lower() in movie.get("overview", "").lower()
        ]

    # search filter
    if q:
        movies = [
            movie for movie in movies
            if q.lower() in movie.get("title", "").lower()
        ]

    return movies[:limit]