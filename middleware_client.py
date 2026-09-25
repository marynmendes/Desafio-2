import requests
import os
from dotenv import load_dotenv

load_dotenv()

MIDDLEWARE_URL = os.getenv("API_URL")


def invoke_agent(user_input: str) -> dict:
    response = requests.post(
        MIDDLEWARE_URL,
        json={
            "input": user_input
        },
        timeout=120
    )

    response.raise_for_status()

    return response.json()