from pathlib import Path

import aws_cdk as cdk
from aws_cdk import Duration, Stack
from aws_cdk import aws_ecr_assets as ecr_assets
from aws_cdk import (
    aws_iam as iam,
)
from aws_cdk import (
    aws_lambda as lambda_,
)
from constructs import Construct

dir_path = Path(__file__).resolve().parent


class DjangoChatbotStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        django_query_handler = lambda_.DockerImageFunction(
            scope=self,
            id="DjangoChatbotQueryHandler",
            function_name="DjangoChatbotQueryHandler",
            code=lambda_.DockerImageCode.from_image_asset(
                directory=str(dir_path.parent / "workspaces" / "retrieval"),
                platform=ecr_assets.Platform.LINUX_AMD64,
            ),
            timeout=Duration.seconds(120),
            memory_size=1024,
            environment={
                "AWS_LWA_INVOKE_MODE": lambda_.InvokeMode.RESPONSE_STREAM.value
            },
        )

        django_query_handler.add_to_role_policy(
            statement=iam.PolicyStatement(
                actions=["ssm:GetParameter"],
                resources=[
                    f"arn:aws:ssm:{self.region}:{self.account}:parameter/django-chatbot/openai-api-key",
                    f"arn:aws:ssm:{self.region}:{self.account}:parameter/django-chatbot/secret-key",
                ],
            )
        )

        function_url = django_query_handler.add_function_url(
            auth_type=lambda_.FunctionUrlAuthType.NONE,
            invoke_mode=lambda_.InvokeMode.RESPONSE_STREAM,
        )

        cdk.CfnOutput(
            self,
            "LambdaFunctionURL",
            value=function_url.url,
        )
