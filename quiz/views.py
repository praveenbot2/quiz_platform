from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render
from .models import Quiz
import openai 
from django.conf import settings 

openai.api_key = settings.OPENAI_API_KEY

def generate_questions(request):
    topic = request.GET.get("topic", "Science")
    num_questions = int(request.GET.get("num", 5))
    prompt = f"Generate {num_questions} multiple-choice questions about {topic}."
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )

    return JsonResponse({"questions": response["choices"][0]["message"]["content"]})


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = User.objects.create_user(username=username, password=password)
        return JsonResponse({"message": "User created successfully"}, status=201)
    return render(request, "register.html")


def create_quiz(request):
    if request.method == "POST":
        title = request.POST["title"]
        category = request.POST["category"]
        quiz = Quiz.objects.create(title=title, category=category)
        return JsonResponse({"message": "Quiz created successfully"})
    return render(request, "create_quiz.html")