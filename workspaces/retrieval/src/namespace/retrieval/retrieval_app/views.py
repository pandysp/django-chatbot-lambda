import httpx
import openai
from django.http import StreamingHttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

OPENAI_MODEL_NAME = "gpt-3.5-turbo-0125"  # gpt-4-turbo-2024-04-09
MODEL_TEMPERATURE = 0.5

client = None


async def index(request):
    return render(request, "index.html")


@require_http_methods(["POST"])
async def answer(request):
    query = request.POST.get("query")

    openai_client = await get_openai_client()
    prompt_value = f"You are an expert for AWS cloud services. Please answer the following question(s): {query}"

    response = StreamingHttpResponse(
        stream_chain(openai_client, prompt_value, OPENAI_MODEL_NAME)
    )

    return response


async def get_openai_client() -> openai.AsyncClient:
    global client
    if client is None or client.is_closed:
        client = httpx.AsyncClient(timeout=120.0, http2=True)
    return openai.AsyncClient(http_client=client)


async def stream_chain(async_client: openai.AsyncClient, prompt_value: str, model: str):
    messages = [{"role": "user", "content": prompt_value}]
    stream = await async_client.chat.completions.create(
        model=model,
        messages=messages,
        stream=True,
        temperature=MODEL_TEMPERATURE,
    )

    async for chunk in stream:
        if chunk.choices:
            yield chunk.choices[0].delta.content  # .encode('utf-8')?
