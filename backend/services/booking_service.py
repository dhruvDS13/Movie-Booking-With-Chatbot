import ast
import csv
import os
import random
from datetime import date, datetime, timedelta
from pathlib import Path
from threading import Lock
from uuid import uuid4


class BookingService:
    def __init__(self) -> None:
        self._lock = Lock()
        self.movies = self._load_movies()
        self.theatres = [
            {"id": 1, "name": "PVR Phoenix", "city": "Mumbai"},
            {"id": 2, "name": "INOX Megaplex", "city": "Delhi"},
            {"id": 3, "name": "Cinepolis Nexus", "city": "Bengaluru"},
            {"id": 4, "name": "Miraj Cinemas", "city": "Pune"},
        ]
        self.shows = self._build_demo_shows()
        self.bookings: dict[str, dict] = {}
        self.booked_seats: dict[int, set[str]] = {
            show["id"]: set(random.sample(self._all_seats(), k=8))
            for show in self.shows
        }

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
                    genres = [item["name"] for item in ast.literal_eval(row.get("genres") or "[]")]
                except (ValueError, SyntaxError, TypeError):
                    genres = []

                movies.append(
                    {
                        "id": int(row["id"]),
                        "title": row.get("title") or row.get("original_title") or "Untitled",
                        "overview": row.get("overview") or "",
                        "genres": genres,
                        "runtime": int(float(row["runtime"] or 0)),
                        "rating": float(row["vote_average"] or 0),
                        "popularity": float(row["popularity"] or 0),
                        "release_date": row.get("release_date") or "",
                    }
                )

        return sorted(movies, key=lambda item: item["popularity"], reverse=True)[:80]

    def _build_demo_shows(self) -> list[dict]:
        shows = []
        show_id = 1000
        running_movies = self.movies[:16]
        times = ["10:30", "13:45", "17:15", "21:00"]
        for day_offset in range(0, 7):
            show_date = (date.today() + timedelta(days=day_offset)).isoformat()
            for index, movie in enumerate(running_movies):
                theatre = self.theatres[index % len(self.theatres)]
                for show_time in times[:2]:
                    shows.append(
                        {
                            "id": show_id,
                            "movie_id": movie["id"],
                            "movie_title": movie["title"],
                            "theatre_id": theatre["id"],
                            "theatre_name": theatre["name"],
                            "city": theatre["city"],
                            "date": show_date,
                            "time": show_time,
                            "price": 220 + (index % 4) * 40,
                        }
                    )
                    show_id += 1
        return shows

    def _all_seats(self) -> list[str]:
        return [f"{row}{num}" for row in "ABCDEF" for num in range(1, 11)]

    def get_movies(self, genre: str | None = None, q: str | None = None, limit: int = 10) -> list[dict]:
        results = self.movies
        if genre:
            genre_lower = genre.lower()
            results = [movie for movie in results if any(genre_lower in g.lower() for g in movie["genres"])]
        if q:
            query = q.lower()
            results = [
                movie
                for movie in results
                if query in movie["title"].lower() or query in movie["overview"].lower()
            ]
        return results[: max(1, min(limit, 30))]

    def get_shows(
        self,
        movie_id: int | None = None,
        theatre_id: int | None = None,
        show_date: str | None = None,
    ) -> list[dict]:
        results = self.shows
        if movie_id:
            results = [show for show in results if show["movie_id"] == movie_id]
        if theatre_id:
            results = [show for show in results if show["theatre_id"] == theatre_id]
        if show_date:
            results = [show for show in results if show["date"] == show_date]
        return results[:50]

    def check_seat_availability(self, show_id: int) -> dict:
        show = self._find_show(show_id)
        booked = sorted(self.booked_seats.get(show_id, set()))
        available = [seat for seat in self._all_seats() if seat not in booked]
        return {"show": show, "booked": booked, "available": available}

    def create_booking(self, show_id: int, user_id: str, seat_numbers: list[str]) -> dict:
        normalized = [seat.strip().upper() for seat in seat_numbers if seat.strip()]
        if not normalized:
            raise ValueError("At least one seat is required.")

        with self._lock:
            show = self._find_show(show_id)
            booked = self.booked_seats.setdefault(show_id, set())
            unavailable = [seat for seat in normalized if seat in booked]
            invalid = [seat for seat in normalized if seat not in self._all_seats()]
            if invalid:
                raise ValueError(f"Invalid seats: {', '.join(invalid)}")
            if unavailable:
                raise ValueError(f"Seats already booked: {', '.join(unavailable)}")

            booked.update(normalized)
            booking = {
                "booking_id": str(uuid4())[:8].upper(),
                "show_id": show_id,
                "user_id": user_id,
                "movie_title": show["movie_title"],
                "theatre_name": show["theatre_name"],
                "date": show["date"],
                "time": show["time"],
                "seat_numbers": normalized,
                "total_amount": show["price"] * len(normalized),
                "status": "confirmed",
                "created_at": datetime.utcnow().isoformat(),
            }
            self.bookings[booking["booking_id"]] = booking
            return booking

    def get_user_bookings(self, user_id: str) -> list[dict]:
        return [booking for booking in self.bookings.values() if booking["user_id"] == user_id]

    def _find_show(self, show_id: int) -> dict:
        for show in self.shows:
            if show["id"] == show_id:
                return show
        raise ValueError("Show not found.")


booking_service = BookingService()
