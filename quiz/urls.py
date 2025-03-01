from django.urls import path
from .views import register, create_quiz, generate_questions

urlpatterns = [
    path("register/", register, name="register"),
    path("create-quiz/", create_quiz, name="create_quiz"),
    path("generate-questions/", generate_questions, name="generate_questions"),
]
