from django.contrib import admin

from .models import *

# Register your models here.


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 1




class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'date_time', 'pub_date', 'number_of_possible_answers')

    inlines = [AnswerInline]


admin.site.register(Room)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
