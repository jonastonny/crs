from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.core.serializers import json
from django.db.models import Count

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic

from vote.forms import VoteRoomForm, VoteQuestiongroupForm, AddQuestionForm, AddAnswerForm
from vote.models import Room, QuestionGroup, Question, Subscription, Answer, Response

from vote.utils import get_pusher


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

    def get(self, request, *args, **kwargs):
        question_obj = Question.objects.get(pk=kwargs['pk'])
        if not question_obj.is_open:
            messages.warning(request, "Question '%s' is not open!" % question_obj.question_text)
            return redirect(question_obj.group)
        return render(request, template_name=self.template_name, context={'question': question_obj})


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
        return redirect(room_obj)

    def get(self, request, *args, **kwargs):
        room_obj = Room.objects.get(pk=kwargs['room'])
        if not room_obj.owner == request.user:
            return redirect(room_obj)
        return render(request, template_name=self.template_name, context={'room': room_obj, 'form': generic.CreateView.get_form_class(self)})


@login_required
def room_edit(request, room):
    room = Room.objects.get(pk=room)
    if not room.owner == request.user:
        return redirect(room)
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
        return HttpResponse('{"message": "Updates are handled through POSTS only"}', status=405)

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
    room_obj = Room.objects.get(pk=room)
    questiongroup_obj = QuestionGroup.objects.get(pk=questiongroup)
    if room_obj.owner == request.user:
        context = {'questiongroup': questiongroup_obj, 'form': VoteQuestiongroupForm(instance=questiongroup_obj)}
        return render(request, 'vote/questiongroup_edit.html', context)
    return redirect(questiongroup_obj)


@login_required
def questiongroup_update(request, room, questiongroup):

    if not request.method == 'POST':
        return HttpResponse(status=403)
    questiongroup = QuestionGroup.objects.get(pk=questiongroup)
    form = VoteQuestiongroupForm(request.POST or None, instance=questiongroup)

    if form.is_valid():
        form.save()
        return redirect(questiongroup)
    return render(request, 'vote/questiongroup_edit.html', {'questiongroup': questiongroup, 'form': form})


def question_answer_create(request, room, questiongroup):
    size = len([k for k in request.POST if 'answer_text' in k])
    room_obj = Room.objects.get(pk=room)
    questiongroup_obj = QuestionGroup.objects.get(pk=questiongroup)
    if not room_obj.owner == request.user:
        return redirect(questiongroup_obj)
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
def question_answer_edit(request, room, questiongroup, question):
    room_obj = Room.objects.get(pk=room)
    question_obj = Question.objects.get(pk=question, group=questiongroup)
    if room_obj.owner == request.user:
        questionform = AddQuestionForm(instance=question_obj)
        answer_set = question_obj.answer_set.all()
        answerforms = [AddAnswerForm(data={'id': obj.id, 'answer_text': obj.answer_text}, instance=Answer.objects.get(id=obj.id)) for obj in answer_set]

        return render(request, 'vote/question_edit.html', {'qform': questionform, 'aforms': answerforms, 'room': room, 'questiongroup': questiongroup, 'question': question, 'q': question_obj})
    else:
        return redirect(question_obj)

@login_required
def question_answer_update(request, room, questiongroup, question):
    if not request.method == 'POST':
        return HttpResponse(status=402)

    if "question_text" in request.POST:
        question_obj = Question.objects.get(id=question)
        questionform = AddQuestionForm(request.POST, instance=question_obj)
        if questionform.is_valid():
            questionform.save()
        return JsonResponse(questionform.errors)

    if "answer_text" in request.POST:
        my_id = request.POST['answer_id']
        if my_id == 'None':
            my_id = None
        (answer_obj, created) = Answer.objects.update_or_create(id=my_id, question_id=question)
        answerform = AddAnswerForm(request.POST, instance=answer_obj)
        if answerform.is_valid():
            answerform.save()
            data = serializers.serialize("json", [answer_obj])
            return JsonResponse(data, safe=False)
        return JsonResponse(answerform.errors)

    # return JsonResponse({"message": "Could not update"})
    return HttpResponse(status=402)


@login_required
def room_delete(request, room):
    if not request.method == 'POST':
        return HttpResponse(403)
    room = Room.objects.get(pk=room)

    if room.owner == request.user:
        messages.info(request, "%s was succesfully removed." % room.title)
        room.delete()
        return redirect('dashboard')
    else:
        messages.error(request, "You are trying to delete a room that you do not own!")
        return redirect(room)


@login_required
def question_delete(request, room, questiongroup, question):
    if not request.method == 'POST':
        return HttpResponse(403)
    room = get_object_or_404(Room, pk=room)
    if room.owner == request.user:
        qg = get_object_or_404(QuestionGroup, pk=questiongroup)
        if qg.room == room:
            question = get_object_or_404(Question, pk=question)
            if question.group == qg:
                (val, d) = question.delete()
                if val > 0:
                    messages.info(request, 'Question deleted.')
                    return redirect(qg)
                else:
                    messages.warning(request, 'Could not delete question.')
                    return redirect(qg)  # Should link to Question instead

    messages.warning(request, 'You are not allowed to delete this question!')
    return redirect(room)  # If anything goes wrong, return not allowed!


@login_required
def answer_delete(request, room, questiongroup, question, answer):
    if not request.method == 'POST':
        return HttpResponse(403)
    room = get_object_or_404(Room, pk=room)
    if room.owner == request.user:
        qg = get_object_or_404(QuestionGroup, pk=questiongroup)
        if qg.room == room:
            question = get_object_or_404(Question, pk=question)
            if question.group == qg:
                answer = get_object_or_404(Answer, pk=answer)
                if answer.question == question:
                    (val, d) = answer.delete()
                    if val > 0:
                        # messages.info(request, 'Answer deleted.')
                        return JsonResponse({'message': 'Answer Deleted'})
                    else:
                        # messages.warning(request, 'Could not delete question.')
                        return JsonResponse({'message': 'Answer could not be deleted'})
    messages.warning(request, 'You are not allowed to delete this answer!')
    return redirect(room)  # If anything goes wrong, return not allowed!


@login_required
def question_response(request, room, questiongroup, question):
    question = Question.objects.get(pk=question)
    return render(request, 'vote/question_response.html', {'room': room, 'questiongroup': questiongroup, 'question': question})


def answer_response(request, room, questiongroup, question):
    if not request.method == 'POST':
        return HttpResponse(403)

    try:
        subscription = Subscription.objects.get(room=room, user=request.user)
    except Subscription.DoesNotExist:
        subscription = None

    room_obj = Room.objects.get(pk=room)
    qg = get_object_or_404(QuestionGroup, pk=questiongroup)
    if subscription or room_obj.owner == request.user and qg.is_open:
        question_obj = get_object_or_404(Question, pk=question)
        if question_obj.is_open:
            answer_obj = get_object_or_404(Answer, pk=request.POST['answer'])
            response, created = Response.objects.update_or_create(question=question_obj, user=request.user, defaults={'answer': answer_obj, 'user': request.user, 'question': question_obj})
            # if created:
            #     return JsonResponse({'message:' 'Response created'}, safe=False)
            # else:
            #     return JsonResponse({'message': 'Response updated'}, safe=False)
            result = question_obj.response_set.all().values('answer_id').annotate(answer_count=Count('answer_id'))
            # result = Answer.objects.filter(question_id=question).annotate(answer_count=Count('response'))
            answer_set = question_obj.answer_set.all()
            myData = {
                'labels': [a.answer_text for a in answer_set],
                'series': [a.number_of_responses() for a in answer_set]
            }
            # for v in result:
            #     myData[v['answer_id']] = v
            # data = serializers.serialize("json", myData)
            event = "response-%s%s%s" % (room, questiongroup, question)
            get_pusher().trigger('crs', event, {'data': myData})
    return redirect(qg)
