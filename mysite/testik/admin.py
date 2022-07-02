from django.contrib import admin
from .models import *


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "parent")
    list_display_links = ("title",)
    list_filter = ("parent",)


class TestAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "created_date", "update_date",
                    "attempts", "category", "time_border", "shuffle")
    search_fields = ("title", "description")
    list_editable = ("shuffle",)
    list_filter = ("created_date", "update_date", "category", "time_border", "shuffle")


class QuestionAdmin(admin.ModelAdmin):
    list_display = ("test_id", "question_text", "question_type")
    search_fields = ("question_text",)
    list_filter = ("question_type",)


class AnswerAdmin(admin.ModelAdmin):
    list_display = ("question_id", "answer_text", "is_correct")
    search_fields = ("answer_text",)
    list_editable = ("is_correct",)
    list_filter = ("is_correct",)


class TestResultAdmin(admin.ModelAdmin):
    list_display = ("id", "user_id", "test_id", "result", "attempt_time")
    list_filter = ("attempt_time",)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Test, TestAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(TestResult, TestResultAdmin)
