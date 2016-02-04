from django.shortcuts import render
from django.views import generic
from vote.models import Room, Question


class RoomDetailView(generic.DetailView):
    template_name = 'vote/room_detail.html'
    model = Room


class QuestionDetailView(generic.DetailView):
    template_name = 'vote/question_detail.html'
    model = Question
