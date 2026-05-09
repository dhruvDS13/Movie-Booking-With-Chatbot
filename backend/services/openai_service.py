import os
from openai import OpenAI
from services.booking_service import booking_service

class OpenAIChatService:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")

        if not api_key:
            raise Exception("OPENAI_API_KEY missing")

        self.client = OpenAI(api_key=api_key)

    def chat(self, user_id: str, message: str) -> str:
        movies = booking_service.get_movies(limit=5)

        movie_list = ", ".join([m["title"] for m in movies]) if movies else "No movies found"

        prompt = f"""
You are a movie booking assistant.

User message: {message}

Available movies:
{movie_list}

Reply naturally and recommend movies or help booking.
"""

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful movie assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )

        return response.choices[0].message.content.strip()


openai_chat_service = OpenAIChatService()