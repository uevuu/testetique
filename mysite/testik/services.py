from .models import Answer, Question


def open_field_answer_validator(answer, correct):
    answer = answer.lower().strip().replace('.', '').replace(',', '').replace(' ', '')
    correct = correct.lower().strip().replace('.', '').replace(',', '').replace(' ', '')
    return answer == correct


def processing_user_answers(request, test_id):
    total = 0
    maximum = 0
    mistakes = []
    questions = Question.objects.filter(test_id=test_id)
    for question in questions:
        if question.question_type == -1:
            maximum += 1
            user_answer = request.POST[f'{question.pk}']
            correct_answer = Answer.objects.get(question_id=question.pk).answer_text
            check = open_field_answer_validator(user_answer, correct_answer)
            if not check:
                mistakes.append((question.question_text, [user_answer]))
            total += check
        elif question.question_type == 0:
            maximum += 1
            user_answer = Answer.objects.get(pk=request.POST[f'{question.pk}'])
            check = user_answer.is_correct
            if not check:
                mistakes.append((question.question_text, [user_answer.answer_text]))
            total += check
        else:
            answers = Answer.objects.filter(question_id=question.pk)
            maximum += len(answers)
            mistake = []
            user_answers = request.POST.getlist(f'{question.pk}')
            for answer in answers:
                if answer.is_correct:
                    if str(answer.pk) in user_answers:
                        total += 1
                    else:
                        mistake.append(answer.answer_text)
                else:
                    if str(answer.pk) in user_answers:
                        mistake.append(answer.answer_text)
                    else:
                        total += 1
            if mistake:
                mistakes.append((question.question_text, mistake))
    return total, maximum, mistakes
