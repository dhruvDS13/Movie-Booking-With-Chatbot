from fastapi import APIRouter

from services.booking_service import booking_service


router = APIRouter(prefix="/shows", tags=["shows"])


@router.get("")
def get_shows(
    movie_id: int | None = None,
    theatre_id: int | None = None,
    date: str | None = None,
):
    return booking_service.get_shows(movie_id=movie_id, theatre_id=theatre_id, show_date=date)


@router.get("/{show_id}/seats")
def get_seats(show_id: int):
    return booking_service.check_seat_availability(show_id)
