# This file needs to be inside the settings module
# otherwise the module will be prioritized over settings.py
import os

env = os.getenv("DJANGO_ENV", "development")

if env == "production":
    from .base_settings.production import *
elif env == "development":
    from .base_settings.development import *
else:
    from .base_settings.development import *
