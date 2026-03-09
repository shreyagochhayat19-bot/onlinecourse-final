from django.shortcuts import render, get_object_or_404
from .models import Course, Enrollment, Question, Choice, Submission


def course_details(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    return render(request, 'onlinecourse/course_details_bootstrap.html', {'course': course})


def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    enrollment = get_object_or_404(Enrollment, user=request.user, course=course)

    submission = Submission.objects.create(enrollment=enrollment)

    selected_ids = []

    for key, value in request.POST.items():
        if key.startswith('choice'):
            choice = get_object_or_404(Choice, pk=value)
            submission.choices.add(choice)
            selected_ids.append(choice.id)

    return show_exam_result(request, submission.id)


def show_exam_result(request, submission_id):
    submission = get_object_or_404(Submission, pk=submission_id)
    enrollment = submission.enrollment
    course = enrollment.course

    selected_choices = submission.choices.all()
    selected_ids = [choice.id for choice in selected_choices]

    grade = 0
    possible = 0

    for question in Question.objects.filter(course=course):
        possible += question.grade
        selected_for_question = [
            choice.id for choice in selected_choices if choice.question == question
        ]

        if question.is_get_score(selected_for_question):
            grade += question.grade

    context = {
        'course': course,
        'submission': submission,
        'selected_ids': selected_ids,
        'grade': grade,
        'possible': possible
    }

    return render(request, 'onlinecourse/exam_result_bootstrap.html', context)
