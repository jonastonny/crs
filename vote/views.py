from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic

from vote.forms import VoteRoomForm, VoteQuestiongroupForm, AddQuestionForm, AddAnswerForm
from vote.models import Room, QuestionGroup, Question, Subscription, Answer


class RoomDetailView(generic.DetailView):
    template_name = 'vote/room_detail.html'
    model = Room


class QuestionGroupDetailView(generic.DetailView):
    template_name = 'vote/questiongroup_detail.html'
    model = QuestionGroup

    def get(self, request, *args, **kwargs):
        qg = get_object_or_404(QuestionGroup, pk=kwargs['pk'])
        if not qg.is_open and request.user != qg.room.owner:
            messages.warning(request, "Group '%s' is not open!" % qg.title)
            return redirect(qg.room)
        return render(request, template_name=self.template_name, context={'questiongroup': qg})


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


def question_answer_create(request, room, questiongroup):
    size = len([k for k in request.POST if 'answer_text' in k])
    if request.method == 'POST':
        questionform = AddQuestionForm(request.POST or None, instance=Question())
        answerform = [AddAnswerForm(request.POST or None, prefix=str(x), instance=Answer()) for x in range(0, size)]
        questionform.instance.group_id = questiongroup

        if questionform.is_valid() and all([af.is_valid() for af in answerform]):
            new_question = questionform.save()
            for af in answerform:
                new_answer = af.save(commit=False)
                new_answer.question = new_question
                new_answer.save()
            return redirect(new_question)

    else:
        questionform = AddQuestionForm()
        answerform = [AddAnswerForm(prefix=str(0), instance=Answer())]

    return render(request, 'vote/question_create.html', {'qform': questionform, 'aforms': answerform, 'room': room, 'questiongroup': questiongroup})

@login_required
def room_delete(request, room):
    if not request.method == 'POST':
        return HttpResponse(201)
    room = Room.objects.get(pk=room)

    if room.owner == request.user:
        messages.info(request, "%s was succesfully removed." % room.title)
        room.delete()
        return redirect('dashboard')
    else:
        messages.error(request, "You are trying to delete a room that you do not own!")
        return redirect(room)

