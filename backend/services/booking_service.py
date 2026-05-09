import ast
import csv
import os
import random
from datetime import date, datetime, timedelta
from pathlib import Path
from threading import Lock
from uuid import uuid4

from config.database import supabase


class BookingService:
    def __init__(self) -> None:
        self._lock = Lock()
        self.movies = self._load_movies()

        self.bookings: dict[str, dict] = {}
        self.booked_seats: dict[str, set[str]] = {}

    def _csv_path(self) -> Path:
        configured = os.getenv("TMDB_MOVIES_CSV", "../tmdb_5000_movies.csv")
        path = Path(configured)

        if not path.is_absolute():
            path = Path(__file__).resolve().parent.parent / path

        return path.resolve()

    def _load_movies(self) -> list[dict]:
        path = self._csv_path()

        if not path.exists():
            return []

        movies = []

        with path.open("r", encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)

            for row in reader:
                try:
                    genres = [
                        item["name"]
                        for item in ast.literal_eval(row.get("genres") or "[]")
                    ]
                except (ValueError, SyntaxError, TypeError):
                    genres = []

                movies.append(
                    {
                        "id": int(row["id"]),
                        "title": row.get("title")
                        or row.get("original_title")
                        or "Untitled",
                        "overview": row.get("overview") or "",
                        "genres": genres,
                        "runtime": int(float(row["runtime"] or 0)),
                        "rating": float(row["vote_average"] or 0),
                        "popularity": float(row["popularity"] or 0),
                        "release_date": row.get("release_date") or "",
                    }
                )

        return sorted(
            movies,
            key=lambda item: item["popularity"],
            reverse=True,
        )[:80]

    def _all_seats(self) -> list[str]:
        return [f"{row}{num}" for row in "ABCDEF" for num in range(1, 11)]

    def get_movies(
        self,
        genre: str | None = None,
        q: str | None = None,
        limit: int = 10,
    ) -> list[dict]:

        results = self.movies

        if genre:
            genre_lower = genre.lower()

            results = [
                movie
                for movie in results
                if any(genre_lower in g.lower() for g in movie["genres"])
            ]

        if q:
            query = q.lower()

            results = [
                movie
                for movie in results
                if query in movie["title"].lower()
                or query in movie["overview"].lower()
            ]

        return results[: max(1, min(limit, 30))]

    def get_shows(
        self,
        movie_id: str | None = None,
        theatre_id: str | None = None,
        show_date: str | None = None,
    ) -> list[dict]:

        query = supabase.table("shows").select("*")

        if movie_id:
            query = query.eq("movie_id", movie_id)

        if theatre_id:
            query = query.eq("theatre_id", theatre_id)

        response = query.execute()

        return response.data

    def check_seat_availability(self, show_id: str) -> dict:

        show_response = (
            supabase.table("shows")
            .select("*")
            .eq("id", show_id)
            .execute()
        )

        if not show_response.data:
            raise ValueError("Show not found.")

        show = show_response.data[0]

        seats_response = (
            supabase.table("seats")
            .select("*")
            .eq("show_id", show_id)
            .execute()
        )

        seats = seats_response.data

        booked = [
            seat["seat_number"]
            for seat in seats
            if seat["is_booked"]
        ]

        available = [
            seat["seat_number"]
            for seat in seats
            if not seat["is_booked"]
        ]

        return {
            "show": show,
            "booked": booked,
            "available": available,
        }

    def create_booking(
        self,
        show_id: str,
        user_id: str,
        seat_numbers: list[str],
    ) -> dict:

        normalized = [
            seat.strip().upper()
            for seat in seat_numbers
            if seat.strip()
        ]

        if not normalized:
            raise ValueError("At least one seat is required.")

        seats_response = (
            supabase.table("seats")
            .select("*")
            .eq("show_id", show_id)
            .execute()
        )

        seats = seats_response.data

        booked_seats = {
            seat["seat_number"]
            for seat in seats
            if seat["is_booked"]
        }

        unavailable = [
            seat
            for seat in normalized
            if seat in booked_seats
        ]

        if unavailable:
            raise ValueError(
                f"Seats already booked: {', '.join(unavailable)}"
            )

        for seat in normalized:
            (
                supabase.table("seats")
                .update({"is_booked": True})
                .eq("show_id", show_id)
                .eq("seat_number", seat)
                .execute()
            )

        show_response = (
            supabase.table("shows")
            .select("*")
            .eq("id", show_id)
            .execute()
        )

        show = show_response.data[0]

        booking = {
            "booking_id": str(uuid4())[:8].upper(),
            "show_id": show_id,
            "user_id": user_id,
            "seat_numbers": normalized,
            "total_amount": show["price"] * len(normalized),
            "status": "confirmed",
            "created_at": datetime.utcnow().isoformat(),
        }

        supabase.table("bookings").insert(booking).execute()

        return booking

    def get_user_bookings(self, user_id: str) -> list[dict]:

        response = (
            supabase.table("bookings")
            .select("*")
            .eq("user_id", user_id)
            .execute()
        )

        return response.data


booking_service = BookingService()