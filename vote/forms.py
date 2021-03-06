from django import forms

from vote.models import Room, Question, Answer, QuestionGroup


class VoteRoomForm(forms.ModelForm):

    class Meta:
        model = Room
        fields = ['title']


class VoteQuestiongroupForm(forms.ModelForm):

    class Meta:
        model = QuestionGroup
        fields = ['title']


class AddQuestionForm(forms.ModelForm):
    # question_text = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Question
        fields = ['question_text']


class AddAnswerForm(forms.ModelForm):
    # answer_text = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Answer
        fields = ['answer_text', 'correct']
