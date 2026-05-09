import os
import requests

TMDB_TOKEN = os.getenv("TMDB_READ_ACCESS_TOKEN")

BASE_URL = "https://api.themoviedb.org/3"

headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {TMDB_TOKEN}"
}


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
            "rating": movie.get("vote_average", 0),
            "genres": ["Trending"],
            "poster": f"https://image.tmdb.org/t/p/w500{movie.get('poster_path')}"
            if movie.get("poster_path")
            else ""
        })

    return movies