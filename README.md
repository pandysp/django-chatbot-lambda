# Django Chatbot with Response Streaming using OpenAI, Langchain and HTMX, deployed to AWS Lambda

## Overview

This is a Django chatbot that uses OpenAI's GPT-3.5 to generate responses. The chatbot is deployed to AWS Lambda using the AWS CDK.

## Features

- Django
- OpenAI
- HTMX
- AWS Lambda
- AWS CDK

## Requirements

- Python 3.12
- Poetry
- AWS CLI

## Installation

To install the required packages, you can use the following command:

```bash
make init
```

## Configuration

You need to create a `.env` file with the following variables:

```bash
OPENAI_API_KEY=your-api-key
AWS_ACCESS_KEY_ID=your-access-key-id
AWS_SECRET_ACCESS_KEY=your-secret-access-key
```

You can copy the `.env.example` file and replace the values with your own.

```bash
cp .env.example .env
```

## Development

### Local

To run the Django server locally, you can use the following commands:

```bash

make run-server
```

The server will be running at `http://localhost:8000`.

### Docker

You can also use docker. Make sure to source the `.env` file and build the docker image:

```bash
make docker-build
make docker-run
```

The server will be running at `http://localhost:9000`.

## Deployment

You need to set the openai api key in the AWS Parameter Store.

```bash
aws ssm put-parameter --name /django-chatbot/openai-api-key --value your-api-key --type String
```

You also need to generate and set a secret key for Django.

```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

Then, set the secret key in the AWS Parameter Store.

```bash
aws ssm put-parameter --name /django-chatbot/secret-key --value your-secret-key --type String
```

Bootstrap the CDK toolkit.

```bash
cdk bootstrap
```

Check potential warnings from django.

```bash
make check-deploy
```

Synthetize the CloudFormation template.

```bash
cdk synth
```

Deploy the CloudFormation template.

```bash
cdk deploy
```
