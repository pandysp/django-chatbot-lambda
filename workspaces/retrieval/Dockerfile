FROM public.ecr.aws/docker/library/python:3.12.0-slim-bullseye
COPY --from=public.ecr.aws/awsguru/aws-lambda-adapter:0.8.1 /lambda-adapter /opt/extensions/lambda-adapter

RUN apt-get update && \
    apt-get install -y gcc g++ && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip install poetry
COPY pyproject.toml poetry.lock* ./

RUN mkdir -p ./src/namespace
RUN touch ./src/namespace/__init__.py

RUN poetry config virtualenvs.create false && \
    poetry install --no-dev

COPY . .

CMD ["uvicorn", "--app-dir=./src/namespace/retrieval" "retrieval.asgi:application", "--host", "0.0.0.0", "--port", "8080"]