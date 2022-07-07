from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


class Category(models.Model):
    title = models.CharField(max_length=50, verbose_name="Категория")
    parent = models.ForeignKey("Category", on_delete=models.SET_NULL, null=True,
                               blank=True, verbose_name="Родительская категория")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "категории"
        ordering = ["title"]

    def get_absolute_url(self):
        # url in template tags
        return reverse('category', kwargs={"category_id": self.pk})


class Test(models.Model):
    title = models.CharField(max_length=150, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    update_date = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    attempts = models.PositiveIntegerField(default=0, verbose_name="Пройдено")
    category = models.ForeignKey("Category", on_delete=models.CASCADE, verbose_name="Категория")
    time_border = models.DurationField(blank=True, null=True, verbose_name="Ограничение по времени")
    shuffle = models.BooleanField(default=False, verbose_name="Перемешать вопросы")

    def get_test_url(self):
        return reverse('test', kwargs={"test_id": self.pk})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "тест"
        verbose_name_plural = "тесты"
        ordering = ["-created_date", "title"]


class Question(models.Model):
    test_id = models.ForeignKey("Test", on_delete=models.CASCADE, verbose_name="Тест")
    question_text = models.TextField(verbose_name="Вопрос")
    question_type = models.SmallIntegerField(default=0, verbose_name="Тип вопроса")

    def __str__(self):
        return self.question_text

    class Meta:
        verbose_name = "вопрос"
        verbose_name_plural = "вопросы"
        ordering = ["question_text"]


class Answer(models.Model):
    question_id = models.ForeignKey("Question", on_delete=models.CASCADE, verbose_name="Вопрос")
    answer_text = models.TextField(blank=True, null=True, verbose_name="Ответ")
    is_correct = models.BooleanField(verbose_name="Правильный")

    def __str__(self):
        return self.answer_text

    class Meta:
        verbose_name = "ответ"
        verbose_name_plural = "ответы"
        ordering = ["answer_text"]


class TestResult(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    test_id = models.ForeignKey("Test", on_delete=models.CASCADE, verbose_name="Тест")
    result = models.PositiveSmallIntegerField(verbose_name="Результат")
    attempt_time = models.DateTimeField(auto_now_add=True, verbose_name="Время попытки")

    def __str__(self):
        return f"{self.result}, {self.attempt_time}"

    class Meta:
        verbose_name = "результат"
        verbose_name_plural = "результаты"
        ordering = ["-attempt_time"]
