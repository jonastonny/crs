from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import generic

from vote.forms import VoteRoomForm
from vote.models import Room, QuestionGroup, Question, Subscription


class RoomDetailView(generic.DetailView):
    template_name = 'vote/room_detail.html'
    model = Room


class QuestionGroupDetailView(generic.DetailView):
    template_name = 'vote/group_detail.html'
    model = QuestionGroup


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


@login_required
def room_edit(request, room):
    room = Room.objects.get(pk=room)
    context = {'room': room, 'form': VoteRoomForm(instance=room)}
    return render(request, 'vote/room_edit.html', context)


@login_required
def room_update(request, room):

    if not request.method == 'POST':
        return HttpResponse(status=201)
    room = Room.objects.get(pk=room)
    form = VoteRoomForm(request.POST or None, instance=room)

    if form.is_valid():
        form.save()
        return redirect(room)
    return render(request, 'vote/room_edit.html', {'room': room, 'form': form})


@login_required
def room_subscribe(request, room):
    if not request.method == 'POST':
        return HttpResponse('{"message": "Updates are handled through POSTS only"}', status=405)
    obj, created = Subscription.objects.get_or_create(user_id=request.user.id, room_id=room)
    if not created:
        obj.delete()
    return HttpResponse(status=201)


@login_required
def question_toggle(request, room, questiongroup, question):
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


# @login_required
# def questiongroup_toggle(request, room, questiongroup, question):
#     if not request.method == 'POST':
#         return HttpResponse('{"message"}: "Updates are handled through POSTS only"}', status=405)
#
#     if request.user.id