.clean-venv:
	rm -rf .venv

.venv:
	poetry config virtualenvs.create true --local
	poetry install --sync --no-root

init: .clean-venv .venv

start-server: .venv
	uvicorn --app-dir=./workspaces/retrieval/src/namespace/retrieval retrieval.asgi:application --reload --reload-include './*.html'

docker-build:
	docker buildx build --platform linux/arm64 -t lambda-retrieval workspaces/retrieval/

docker-run:
	docker run --platform linux/arm64 -e AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY -e AWS_SESSION_TOKEN -e OPENSEARCH_MASTER_USER_PASSWORD -e OPENAI_API_KEY -e OPENAI_ORGANIZATION -e AWS_EXECUTION_ENV -p 9000:8080 lambda-retrieval