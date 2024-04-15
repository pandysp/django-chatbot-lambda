from .base import *
import boto3

DEBUG = False
# TODO: Consider removing localhost, but it's useful for testing with docker
ALLOWED_HOSTS = [".lambda-url.eu-central-1.on.aws", "localhost"]

SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_SSL_REDIRECT = True

ssm = boto3.client("ssm")
SECRET_KEY = "ssm.get_parameter(Name='/django-chatbot/secret-key', WithDecryption=True)['Parameter']['Value']"

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
