import json
import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("API_URL")


with open("red_team_dataset.json", "r", encoding="utf-8") as f:
    attacks = json.load(f)


results = []

for attack in attacks:

    response = requests.post(
        API_URL,
        json={
            "input": attack["prompt"]
        },
        timeout=180
    )

    result = {
        "id": attack["id"],
        "category": attack["category"],
        "prompt": attack["prompt"],
        "expected_behavior": attack["expected_behavior"],
        "severity": attack["severity"],
        "status_code": response.status_code,
        "response": response.json() if response.ok else response.text
    }

    results.append(result)


with open("response_redteam_novo.json", "w", encoding="utf-8") as f:
    json.dump(
        results,
        f,
        ensure_ascii=False,
        indent=2
    )