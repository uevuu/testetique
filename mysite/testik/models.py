from django.db import models


class Test(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    attempts = models.PositiveIntegerField()
    category = models.ForeignKey("Category", on_delete=models.CASCADE)
    time_border = models.TimeField()


class Question(models.Model):
    test_id = models.ForeignKey("Test", on_delete=models.CASCADE)
    question_text = models.TextField()
    question_type = models.SmallIntegerField()


class Answer(models.Model):
    question_id = models.ForeignKey("Question", on_delete=models.CASCADE)
    answer_text = models.TextField()
    is_correct = models.BooleanField()


class TestResult(models.Model):
    user_id = models.ForeignKey("User", on_delete=models.CASCADE)
    test_id = models.ForeignKey("Test", on_delete=models.CASCADE)
    result = models.PositiveSmallIntegerField()
    attempt_time = models.DateTimeField(auto_now_add=True)


class Category(models.Model):
    title = models.CharField(max_length=50)
    parent = models.ForeignKey("Category", on_delete=models.SET_NULL)
