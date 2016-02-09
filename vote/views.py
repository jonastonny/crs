from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import generic

from vote.forms import VoteRoomForm, VoteQuestiongroupForm
from vote.models import Room, QuestionGroup, Question, Subscription


class RoomDetailView(generic.DetailView):
    template_name = 'vote/room_detail.html'
    model = Room


class QuestionGroupDetailView(generic.DetailView):
    template_name = 'vote/questiongroup_detail.html'
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


class CreateQuestionGroupView(generic.CreateView):
    template_name = 'vote/questiongroup_create.html'
    model = QuestionGroup
    fields = ['title']

    def form_valid(self, form):
        room_obj = Room.objects.get(pk=self.kwargs['room'])
        if room_obj.owner_id == self.request.user.id:
            form.instance.room = room_obj
            return super(CreateQuestionGroupView, self).form_valid(form)


class CreateQuestionView(generic.CreateView):
    template_name = 'vote/question_create.html'
    model = Question
    fields = ['question_text']

    def form_valid(self, form):
        questiongroup_obj = QuestionGroup.objects.get(pk=self.kwargs['questiongroup'])
        room_obj = Room.objects.get(pk=questiongroup_obj.room_id)
        ''' if user is owner of the room, then you are allowed to create questions in question groups '''
        if room_obj.owner_id == self.request.user.id:
            form.instance.room = room_obj
            form.instance.group_id = questiongroup_obj.id
            return super(CreateQuestionView, self).form_valid(form)


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


@login_required
def questiongroup_toggle(request, room, questiongroup):
    if not request.method == 'POST':
        return HttpResponse('{"message"}: "Updates are handled through POSTS only"}', status=405)

    room_obj = Room.objects.get(id=room)
    if request.user.id == room_obj.owner_id:
        questiongroup_obj = QuestionGroup.objects.get(id=questiongroup)
        bool_status = questiongroup_obj.is_open
        questiongroup_obj.is_open = not bool_status
        questiongroup_obj.save()
        return HttpResponse(status=201)
    else:
        return HttpResponse(status=403)


@login_required
def questiongroup_edit(request, room, questiongroup):
    questiongroup_obj = QuestionGroup.objects.get(pk=questiongroup)
    context = {'questiongroup': questiongroup_obj, 'form': VoteQuestiongroupForm(instance=questiongroup_obj)}
    return render(request, 'vote/questiongroup_edit.html', context)


@login_required
def questiongroup_update(request, room, questiongroup):

    if not request.method == 'POST':
        return HttpResponse(status=201)
    questiongroup = QuestionGroup.objects.get(pk=questiongroup)
    form = VoteQuestiongroupForm(request.POST or None, instance=questiongroup)

    if form.is_valid():
        form.save()
        return redirect(questiongroup)
    return render(request, 'vote/questiongroup_edit.html', {'questiongroup': questiongroup, 'form': form})
