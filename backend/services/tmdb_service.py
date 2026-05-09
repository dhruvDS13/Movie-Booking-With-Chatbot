import os
import requests

TMDB_TOKEN = os.getenv("TMDB_READ_ACCESS_TOKEN")

headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {TMDB_TOKEN}"
}

BASE_URL = "https://api.themoviedb.org/3"


def get_trending_movies():
    url = f"{BASE_URL}/trending/movie/day"

    response = requests.get(url, headers=headers)

    data = response.json()

    movies = []

    for movie in data.get("results", []):
        movies.append({
            "id": movie.get("id"),
            "title": movie.get("title"),
            "overview": movie.get("overview"),
            "rating": movie.get("vote_average"),
            "poster": f"https://image.tmdb.org/t/p/w500{movie.get('poster_path')}"
        })

    return movies