from django import forms

from vote.models import Room


class VoteRoomForm(forms.ModelForm):

    class Meta:
        model = Room
        fields = ['title']