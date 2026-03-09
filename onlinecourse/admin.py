from django.contrib import admin
from .models import Course, Lesson, Instructor, Learner, Enrollment, Question, Choice, Submission


class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 2


class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'pub_date')
    list_filter = ('pub_date',)
    search_fields = ('name',)
    inlines = [LessonInline, QuestionInline]


class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]


class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'course')


admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Instructor)
admin.site.register(Learner)
admin.site.register(Enrollment)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Submission)
