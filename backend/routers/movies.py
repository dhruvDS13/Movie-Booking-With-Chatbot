from fastapi import APIRouter, Query

from services.booking_service import booking_service


router = APIRouter(prefix="/movies", tags=["movies"])


@router.get("")
def get_movies(
    genre: str | None = None,
    q: str | None = None,
    limit: int = Query(default=12, ge=1, le=30),
):
    return booking_service.get_movies(genre=genre, q=q, limit=limit)
