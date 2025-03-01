from django.contrib.auth.models import AbstractUser,Permission
from django.db import models

class User(AbstractUser):
    is_admin = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        "auth.Group",
        related_name="quiz_users",  # Change related_name to avoid conflicts
        blank=True
    )
    
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="quiz_users_permissions",  # Change related_name
        blank=True
    )
class Quiz(models.Model):
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=100)

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    text = models.TextField()
    option1 = models.CharField(max_length=255)
    option2 = models.CharField(max_length=255)
    option3 = models.CharField(max_length=255)
    option4 = models.CharField(max_length=255)
    correct_option = models.IntegerField()
