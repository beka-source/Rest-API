"""Default configuration

Use env var to override
"""
import os
from datetime import timedelta


ENV = os.getenv("FLASK_ENV")
DEBUG = ENV == "development"
SECRET_KEY = os.getenv("SECRET_KEY")

SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI")
SQLALCHEMY_TRACK_MODIFICATIONS = False

JWT_BLACKLIST_ENABLED = True
JWT_BLACKLIST_TOKEN_CHECKS = ["access", "refresh"]

ACCESS_EXPIRES = timedelta(minutes=1000)
JWT_ACCESS_TOKEN_EXPIRES = ACCESS_EXPIRES

CELERY = {
    "broker_url": os.getenv("CELERY_BROKER_URL"),
    "result_backend": os.getenv("CELERY_RESULT_BACKEND_URL"),
}

REGEX_MOBILE_KZ = "^7[740][0125678][0-9][0-9][0-9][0-9][0-9][0-9][0-9]"
SEND_SMS_KZ = "QAZNA ONLINE, \nҚұрметті Қолдануші: \nСізге жіберлген код:"
SEND_SMS_RU = "QAZNA ONLINE, \nҚұрметті Қолдануші: \nСізге жіберлген код:"
