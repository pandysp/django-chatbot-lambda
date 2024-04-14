from django.shortcuts import render


async def index(request):
    return render(request, "index.html")


async def answer(request):
    user_input = request.POST.get("user-input")
    answer = "I don't know the answer to that question."
    
    return render(request, "answer.html", {"user_input": user_input, "answer": answer})
