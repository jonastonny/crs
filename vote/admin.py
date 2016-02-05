from django.contrib import admin
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from super_inlines.admin import SuperInlineModelAdmin, SuperModelAdmin

from .models import *

# Register your models here.


class ResponseInline(SuperInlineModelAdmin, admin.TabularInline):
    model = Response
    extra = 0
    fields = ['answer', 'user', 'date_time']
    readonly_fields = ['answer', 'user', 'date_time']


class AnswerInline(SuperInlineModelAdmin, admin.TabularInline):
    model = Answer
    extra = 0
    # inlines = [ResponseInline]
    fields = ('answer_text', 'number_of_responses', 'response_link')
    readonly_fields = ['number_of_responses', 'date_time', 'response_link']

    def response_link(self, obj):
        return mark_safe("<a href='%s'>Show Responses</a>" % reverse('admin:vote_response_changelist', ))

    response_link.allow_tags = True


class QuestionAdmin(admin.ModelAdmin):
    search_fields = ['question_text']
    list_display = ('question_text',
                    'date_time',
                    'pub_date',
                    'total_responses')

    inlines = [AnswerInline]

    # readonly_fields = ['room', ]
    model = Question


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 0
    #inlines = [AnswerInline]
    readonly_fields = ['question_text', 'date_time', 'pub_date']
    max_num = 0



class RoomAdmin(admin.ModelAdmin):
    search_fields = ['title']
    inlines = [QuestionInline]


admin.site.register(Room, RoomAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)
admin.site.register(Response)