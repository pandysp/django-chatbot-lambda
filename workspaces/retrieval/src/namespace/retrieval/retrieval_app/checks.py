import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from django.core.checks import Error, register

from .utils import fetch_secret


@register()
def check_openai_key(app_configs, **kwargs):
    key = fetch_secret("/django-chatbot/openai-api-key")
    if not key:
        return [
            Error(
                "OPENAI_API_KEY is not set.",
                hint="Check the AWS Parameter Store settings and connectivity.",
                id="retrieval_app.E001",
            )
        ]
    return []


@register()
def check_aws_credentials(app_configs, **kwargs):
    errors = []
    try:
        # Attempt to create a client to check credentials
        client = boto3.client("sts")
        client.get_caller_identity()  # This does not incur any costs but requires valid credentials
    except NoCredentialsError:
        errors.append(
            Error(
                "No AWS credentials found.",
                hint="Ensure that AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY are properly set.",
                id="yourapp.E002",
            )
        )
    except PartialCredentialsError:
        errors.append(
            Error(
                "Incomplete AWS credentials found.",
                hint="Ensure that both AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY are properly set.",
                id="yourapp.E003",
            )
        )
    return errors
