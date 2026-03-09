from django.shortcuts import render, get_object_or_404
from .models import Course, Enrollment, Question, Choice, Submission


def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    enrollment = get_object_or_404(Enrollment, user=request.user, course=course)

    submission = Submission.objects.create(enrollment=enrollment)

    selected_choices = []

    for key, value in request.POST.items():
        if key.startswith('choice'):
            choice = get_object_or_404(Choice, pk=value)
            submission.choices.add(choice)
            selected_choices.append(choice)

    return show_exam_result(request, submission.id)


def show_exam_result(request, submission_id):
    submission = get_object_or_404(Submission, pk=submission_id)
    enrollment = submission.enrollment
    course = enrollment.course

    selected_choices = submission.choices.all()

    total_score = 0
    user_score = 0

    for question in Question.objects.filter(course=course):
        total_score += question.grade

        correct_choices = set(question.choice_set.filter(is_correct=True))
        selected = set(selected_choices.filter(question=question))

        if correct_choices == selected:
            user_score += question.grade

    percentage = 0
    if total_score > 0:
        percentage = (user_score / total_score) * 100

    passed = percentage >= 50

    context = {
        'course': course,
        'score': user_score,
        'total': total_score,
        'percentage': percentage,
        'passed': passed,
        'submission': submission
    }

    return render(request, 'onlinecourse/exam_result.html', context)