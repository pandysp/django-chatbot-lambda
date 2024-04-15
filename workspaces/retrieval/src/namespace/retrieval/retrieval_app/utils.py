import os

import boto3
from botocore.exceptions import ClientError


def fetch_secret(name: str) -> str | None:
    """Fetch secret from AWS Parameter Store."""
    client = boto3.client("ssm", region_name="eu-central-1")
    try:
        response = client.get_parameter(Name=name, WithDecryption=True)

        return response["Parameter"]["Value"]
    except ClientError as e:
        print(f"An error occurred: {e}")
        return None


def set_api_key() -> None:
    try:
        key = fetch_secret("/django/openai-key")
        if key:
            os.environ["OPENAI_API_KEY"] = key
        else:
            raise ValueError(
                "Failed to fetch the OPENAI_API_KEY. Application cannot start."
            )
    except ValueError:
        if os.getenv("DJANGO_ENV") == "production":
            raise
        else:
            if not os.environ.get("OPENAI_API_KEY"):
                raise ValueError("OPENAI_API_KEY development key not set.")

            print("Using OPENAI_API_KEY development key.")
