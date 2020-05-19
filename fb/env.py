import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
DATABASE_URL = os.getenv('DATABASE_URL')
LOG_LEVEL = os.getenv('LOG_LEVEL') or 'INFO'
FREQUENCY = int(os.getenv('FREQUENCY')) or 60
TRAVEL_FREQUENCY = int(os.getenv('FREQUENCY')) or 60
DRUGS_CHANNEL = int(os.getenv('DRUGS_CHANNEL'))
FLOWERS_CHANNEL = int(os.getenv('FLOWERS_CHANNEL'))
PLUSHIES_CHANNEL = int(os.getenv('PLUSHIES_CHANNEL'))
SENTRY_DSN = os.getenv('SENTRY_DSN')
