from os import environ, getenv

# Not used in web app, so can be None in that container
TELEGRAM_TOKEN = getenv("TELEGRAM_TOKEN")

APP_PWD = environ["APP_PWD"]
APP_SECRET_KEY = environ["APP_SECRET_KEY"]
GOOGLE_CLOUD_PROJECT = environ["GOOGLE_CLOUD_PROJECT"]
GOOGLE_APPLICATION_CREDENTIALS = environ["GOOGLE_APPLICATION_CREDENTIALS"]
