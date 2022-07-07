from django.core.exceptions import ValidationError


def question_type_validator(value):
    if value not in (-1, 0, 1):
        raise ValidationError(f"{value} не является типом вопроса")
