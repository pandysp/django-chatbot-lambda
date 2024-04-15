import os
import aws_cdk as cdk

from django_chatbot.django_chatbot_stack import DjangoChatbotStack

app = cdk.App()
DjangoChatbotStack(
    app,
    "DjangoChatbotStack",
    env=cdk.Environment(
        region=os.environ.get("CDK_DEFAULT_REGION", "eu-central-1"),
        account=os.environ.get("CDK_DEFAULT_ACCOUNT"),
    ),
)

app.synth()
