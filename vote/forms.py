from django import forms

from vote.models import Room, Question, Answer


class VoteRoomForm(forms.ModelForm):

    class Meta:
        model = Room
        fields = ['title']


class VoteQuestiongroupForm(forms.ModelForm):

    class Meta:
        model = Room
        fields = ['title']


class AddQuestionForm(forms.ModelForm):

    class Meta:
        model = Question
        fields = ['question_text']


class AddAnswerForm(forms.ModelForm):

    class Meta:
        model = Answer
        fields = ['answer_text']
