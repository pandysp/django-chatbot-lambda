from jinja2 import Environment

from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import reverse


def environment(**options):
    env = Environment(**options)
    env.globals.update(
        {
            "static": staticfiles_storage.url,  # Adding Django's static files function
            "url": reverse,  # Adding Django's URL reverse function
        }
    )
    return env
