from fastapi import APIRouter, HTTPException

from schemas.api import BookingRequest
from services.booking_service import booking_service


router = APIRouter(prefix="/bookings", tags=["bookings"])


@router.post("")
def create_booking(payload: BookingRequest):
    try:
        return booking_service.create_booking(
            show_id=payload.show_id,
            user_id=payload.user_id,
            seat_numbers=payload.seat_numbers,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/{user_id}")
def get_user_bookings(user_id: str):
    return booking_service.get_user_bookings(user_id)
