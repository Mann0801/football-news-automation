import os
from dotenv import load_dotenv

load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
FOOTBALL_DATA_API_KEY = os.getenv("FOOTBALL_DATA_API_KEY")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")
GMAIL_ADDRESS = os.getenv("GMAIL_ADDRESS")
RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL")

LEAGUE_IDS = {
    "Premier League": "PL",
    "La Liga": "PD",
    "Champions League": "CL"
}

EMAIL_SUBJECT_PREFIX = "⚽"
