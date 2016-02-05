from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views import generic
from vote.models import Room, Question, Subscription


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


class EditRoomDetailView(generic.DetailView):
    template_name = 'vote/room_edit.html'
    model = Room


@login_required
def subscribe(request, room):
    if not request.method == 'POST':
        return HttpResponse('{"message": "Updates are handled through POSTS only"}', status=405)
    obj, created = Subscription.objects.get_or_create(user_id=request.user.id, room_id=room)
    if not created:
        obj.delete()
    return HttpResponse(status=201)


@login_required
def question_toggle(request, room, question):
    if not request.method == 'POST':
        return HttpResponse('{"message": "Updates are handled through POSTS only"}', status=405)

    room_obj = Room.objects.get(id=room)
    if request.user.id == room_obj.owner_id:
        question_obj = Question.objects.get(id=question)
        bool_status = question_obj.is_open
        question_obj.is_open = not bool_status
        question_obj.save()
        return HttpResponse(status=201)
    else:
        return HttpResponse(status=403)
