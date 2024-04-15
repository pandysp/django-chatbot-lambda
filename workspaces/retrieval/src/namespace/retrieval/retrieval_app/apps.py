from django.apps import AppConfig


class RetrievalAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "retrieval_app"

    def ready(self):
        from . import checks

        from .utils import set_api_key

        set_api_key()
