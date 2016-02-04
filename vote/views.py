
from django.views import generic
from vote.models import Room, Question


class RoomDetailView(generic.DetailView):
    template_name = 'vote/room_detail.html'
    model = Room


class QuestionDetailView(generic.DetailView):
    template_name = 'vote/question_detail.html'
    model = Question


class CreateRoomView(generic.CreateView):
    template_name = 'vote/room_create.html'

    model = Room
    fields = ['title']

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(CreateRoomView, self).form_valid(form)