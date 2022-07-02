from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Category(models.Model):
    title = models.CharField(max_length=50)
    parent = models.ForeignKey("Category", on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.title


class Test(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    attempts = models.PositiveIntegerField(default=0)
    category = models.ForeignKey("Category", on_delete=models.CASCADE)
    time_border = models.DurationField()

    def __str__(self):
        return self.title


class Question(models.Model):
    test_id = models.ForeignKey("Test", on_delete=models.CASCADE)
    question_text = models.TextField()
    question_type = models.SmallIntegerField()

    def __str__(self):
        return self.question_text


class Answer(models.Model):
    question_id = models.ForeignKey("Question", on_delete=models.CASCADE)
    answer_text = models.TextField()
    is_correct = models.BooleanField()

    def __str__(self):
        return self.answer_text


class TestResult(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    test_id = models.ForeignKey("Test", on_delete=models.CASCADE)
    result = models.PositiveSmallIntegerField()
    attempt_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.result}, {self.attempt_time}"
