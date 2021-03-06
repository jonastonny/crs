import bleach
import short_url
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core import serializers

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.html import strip_tags
from django.views import generic
from django.views.decorators.cache import cache_page

from vote.forms import VoteRoomForm, VoteQuestiongroupForm, AddQuestionForm, AddAnswerForm
from vote.models import Room, QuestionGroup, Question, Subscription, Answer, Response
from vote.templatetags.vote_extras import user_is_subscribed_to_room, room_is_owned_by_user

from vote.utils import get_pusher


ALLOWED_TAGS = [
    'pre',
    'br',
    'p', 
    'em', 
    'strong', 
    'b', 
    'i',
    'u',
    'code',
    'a'
    ]


ALLOWED_ATTRIBUTES = {
    '*': ['class'],
    'p': ['style'],
    'a': ['href'],
}

ALLOWED_STYLES = ['text-align']


class RoomDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = 'vote/room_detail.html'
    model = Room


class QuestionDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = 'vote/question_detail.html'
    model = Question

    def get(self, request, *args, **kwargs):

        question_obj = get_object_or_404(Question, pk=kwargs['pk'])
        room_obj = get_object_or_404(Room, pk=question_obj.group.room.id)
        answer_set = question_obj.answer_set.all()
        # Requester is owner - owners should always be allowed access
        if room_obj.owner == request.user:
            return render(request, template_name=self.template_name, context={'question': question_obj})
        # Requester is not owner and not subscribed - tell them to subscribe
        elif not user_is_subscribed_to_room(request.user, room_obj):
            messages.warning(request, "Subscribe to the room to see questions!")
            return redirect(room_obj)
        # Requester is not owner but subscribed and group and question is open - let them answer!
        elif question_obj.group.is_open and question_obj.is_open:
            return render(request, template_name=self.template_name, context={'question': question_obj})
        # Above failed, but requester have once answered the given question and question or group is now closed
                                # Get's the users who have responded to a question (by getting all answers, all responses and all users)
        elif request.user.id in [item for sublist in [[response.user_id for response in answer.response_set.all()] for answer in answer_set] for item in sublist]:
            return render(request, template_name=self.template_name, context={'question': question_obj})
        # Everything failed, you are not allowed in here.
        else:
            messages.warning(request, "Question '%s' is not open!" % question_obj.question_text[0:50])
            return redirect(question_obj.group)


class CreateRoomView(LoginRequiredMixin, generic.CreateView):
    template_name = 'vote/room_create.html'
    model = Room
    fields = ['title']

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(CreateRoomView, self).form_valid(form)


# class CreateQuestionGroupView(generic.CreateView):
#     template_name = 'vote/questiongroup_create.html'
#     model = QuestionGroup
#     fields = ['title']
#
#     def form_valid(self, form):
#         room_obj = get_object_or_404(Room, pk=self.kwargs['room'])
#         if room_obj.owner_id == self.request.user.id:
#             form.instance.room = room_obj
#             return super(CreateQuestionGroupView, self).form_valid(form)
#         return redirect(room_obj)
#
#     def form_invalid(self, form):
#         room_obj = get_object_or_404(Room, pk=self.kwargs['room'])
#         # form.instance.room = room_obj
#         # form.save()
#         self.get(self.request, form)
#
#     def get(self, request, *args, **kwargs):
#         room_obj = get_object_or_404(Room, pk=kwargs['room'])
#         if not room_obj.owner == request.user:
#             return redirect(room_obj)
#         return render(request, template_name=self.template_name, context={'room': room_obj, 'form': generic.CreateView.get_form_class(self)})


@login_required
def questingroup_create(request, room):
    room = Room.objects.get(pk=room)
    if request.method == 'POST':
        if not room.owner_id == request.user.id:
            return redirect(room)
        form = VoteQuestiongroupForm(request.POST)
        if form.is_valid():
            form.instance.owner_id = request.user.id
            form.instance.room_id = room.id
            qg = form.save()
            return redirect(qg)
        else:
            context = {'room': room, 'form': form}
    else:
        context = {'room': room, 'form': VoteQuestiongroupForm()}

    return render(request, 'vote/questiongroup_create.html', context=context)


@login_required
def room_edit(request, room):
    room = get_object_or_404(Room, pk=room)
    if not room.owner == request.user:
        return redirect(room)
    context = {'room': room, 'form': VoteRoomForm(instance=room)}
    return render(request, 'vote/room_edit.html', context)


@login_required
def room_update(request, room):
    if not request.method == 'POST':
        return HttpResponse(status=201)
    room = get_object_or_404(Room, pk=room)
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

    room_obj = get_object_or_404(Room, id=room)
    if request.user.id == room_obj.owner_id:
        question_obj = get_object_or_404(Question, id=question)
        bool_status = question_obj.is_open
        question_obj.is_open = not bool_status
        question_obj.save()
        return HttpResponse(status=201)
    else:
        return HttpResponse(status=403)


class QuestionGroupDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = 'vote/questiongroup_detail.html'
    model = QuestionGroup

    def get(self, request, *args, **kwargs):
        qg = get_object_or_404(QuestionGroup, pk=kwargs['pk'])
        my_short_url = short_url.encode_url(qg.id)
        context = {'questiongroup': qg, 'short_url': my_short_url}
        if not qg.is_open and request.user != qg.room.owner:
            messages.warning(request, "Group '%s' is not open!" % qg.title)
            return redirect(qg.room)
        elif room_is_owned_by_user(qg.room, request.user):
            return render(request, template_name=self.template_name, context=context)
        elif not user_is_subscribed_to_room(request.user, qg.room):
            messages.warning(request, "Subscribe to see groups!")
            return redirect(qg.room)
        return render(request, template_name=self.template_name, context=context)


@login_required
def questiongroup_toggle(request, room, questiongroup):
    if not request.method == 'POST':
        return HttpResponse('{"message": "Updates are handled through POSTS only"}', status=405)

    room_obj = get_object_or_404(Room, id=room)
    if request.user.id == room_obj.owner_id:
        questiongroup_obj = get_object_or_404(QuestionGroup, id=questiongroup)
        bool_status = questiongroup_obj.is_open
        questiongroup_obj.is_open = not bool_status
        questiongroup_obj.save()
        return HttpResponse(status=201)
    else:
        return HttpResponse(status=403)


@login_required
def questiongroup_edit(request, room, questiongroup):
    room_obj = get_object_or_404(Room, pk=room)
    questiongroup_obj = get_object_or_404(QuestionGroup, pk=questiongroup)
    if room_obj.owner == request.user:
        context = {'questiongroup': questiongroup_obj, 'form': VoteQuestiongroupForm(instance=questiongroup_obj)}
        return render(request, 'vote/questiongroup_edit.html', context)
    return redirect(questiongroup_obj)


@login_required
def questiongroup_update(request, room, questiongroup):

    if not request.method == 'POST':
        return HttpResponse(status=403)
    questiongroup = get_object_or_404(QuestionGroup, pk=questiongroup)
    form = VoteQuestiongroupForm(request.POST or None, instance=questiongroup)

    if form.is_valid():
        form.save()
        return redirect(questiongroup)
    return render(request, 'vote/questiongroup_edit.html', {'questiongroup': questiongroup, 'form': form})


@login_required
def questiongroup_delete(request, room, questiongroup):
    if request.method == 'POST':
        questiongroup = get_object_or_404(QuestionGroup, pk=questiongroup)
        if request.user == questiongroup.room.owner:
            questiongroup.delete()
            return redirect(questiongroup.room)
    else:
        return HttpResponse(status=403)

    messages.error(request, "You are not allowed to delete this group!")
    return redirect('dashboard')


@login_required
def question_answer_create(request, room, questiongroup):
    size = len([k for k in request.POST if 'answer_text' in k])
    room_obj = get_object_or_404(Room, pk=room)
    questiongroup_obj = get_object_or_404(QuestionGroup, pk=questiongroup)

    if not room_obj.owner == request.user:
        return redirect(questiongroup_obj)
    if request.method == 'POST':
        questionform = AddQuestionForm(request.POST or None, instance=Question())
        answerform = [AddAnswerForm(request.POST or None, prefix=str(x), instance=Answer()) for x in range(0, size)]
        questionform.instance.group_id = questiongroup

        if questionform.is_valid() and all([af.is_valid() for af in answerform]):
            new_question = questionform.save(commit=False)
            new_question.question_text = bleach.clean(new_question.question_text, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES, styles=ALLOWED_STYLES)
            new_question.save()
            for af in answerform:
                new_answer = af.save(commit=False)
                # af.cleaned_data['answer_text'] = bleach.clean(af.cleaned_data['answer_text'])
                new_answer.answer_text = bleach.clean(new_answer.answer_text, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES, styles=ALLOWED_STYLES)
                new_answer.question = new_question
                new_answer.save()
            return redirect(new_question)

    else:
        questionform = AddQuestionForm()
        answerform = [AddAnswerForm(prefix=str(0), instance=Answer())]

    return render(request, 'vote/question_create.html', {'qform': questionform, 'aforms': answerform, 'room': room, 'questiongroup': questiongroup, 'qg': questiongroup_obj})


@login_required
def question_answer_edit(request, room, questiongroup, question):
    room_obj = get_object_or_404(Room, pk=room)
    # question_obj = get_object_or_404(Question, pk=question, group=questiongroup)
    question_obj = room_obj.questiongroup_set.get(pk=questiongroup).question_set.get(pk=question)
    # question_obj = Question.objects.get(pk=question, group=questiongroup)
    if room_obj.owner == request.user:
        questionform = AddQuestionForm(instance=question_obj)
        answer_set = question_obj.answer_set.all()
        answerforms = [AddAnswerForm(data={'id': obj.id, 'answer_text': obj.answer_text, 'correct': obj.correct}, instance=get_object_or_404(Answer, id=obj.id)) for obj in answer_set]

        return render(request, 'vote/question_edit.html', {'qform': questionform, 'aforms': answerforms, 'room': room, 'questiongroup': questiongroup, 'question': question, 'q': question_obj})
    else:
        return redirect(question_obj)


@login_required
def question_answer_update(request, room, questiongroup, question):
    if not request.method == 'POST':
        return HttpResponse(status=402)

    if "question_text" in request.POST:
        question_obj = get_object_or_404(Question, id=question)

        # question_obj = Question.objects.get(id=question)
        questionform = AddQuestionForm(request.POST, instance=question_obj)
        if questionform.is_valid():
            questionform.instance.question_text = bleach.clean(questionform.instance.question_text, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES, styles=ALLOWED_STYLES)
            questionform.save()
        return JsonResponse(questionform.errors)

    if "answer_text" in request.POST:
        my_id = request.POST['answer_id']
        if my_id == 'None':
            my_id = None

        answerform = AddAnswerForm(request.POST)
        if answerform.is_valid():
            (answer_obj, created) = Answer.objects.update_or_create(id=my_id,
                                                                    question_id=question,
                                                                    defaults={'answer_text': bleach.clean(answerform.instance.answer_text, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES, styles=ALLOWED_STYLES),
                                                                                                              'correct': answerform.instance.correct})
            data = serializers.serialize("json", [answer_obj])
            return JsonResponse(data, safe=False)
        return JsonResponse(answerform.errors)

    # return JsonResponse({"message": "Could not update"})
    return HttpResponse(status=402)


@login_required
def room_delete(request, room):
    if not request.method == 'POST':
        return HttpResponse(403)
    room = get_object_or_404(Room, pk=room)

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
        qg = room.questiongroup_set.get(pk=questiongroup)
        if qg.room == room:
            question = qg.question_set.get(pk=question)
            if question.group == qg:
                (val, d) = question.delete()
                if val > 0:
                    messages.info(request, 'Question deleted.')
                    return redirect(qg)
                else:
                    messages.warning(request, 'Could not delete question.')
                    return redirect(question)  # Should link to Question instead

    messages.warning(request, 'You are not allowed to delete this question!')
    return redirect(room)  # If anything goes wrong, return not allowed!


@login_required
def answer_delete(request, room, questiongroup, question, answer):
    if not request.method == 'POST':
        return HttpResponse(403)
    room = get_object_or_404(Room, pk=room)
    if room.owner == request.user:
        qg = room.questiongroup_set.get(pk=questiongroup)
        if qg.room == room:
            question = qg.question_set.get(pk=question)
            if question.group == qg:
                answer = question.answer_set.get(pk=answer)
                if answer.question == question:
                    (val, d) = answer.delete()
                    if val > 0:
                        return JsonResponse({'message': 'Answer Deleted'})
                    else:
                        return JsonResponse({'message': 'Answer could not be deleted'})
    messages.warning(request, 'You are not allowed to delete this answer!')
    return redirect(room)  # If anything goes wrong, return not allowed!


@login_required
@cache_page(30)
def question_response(request, room, questiongroup, question):
    room_obj = get_object_or_404(Room, pk=room)
    question = room_obj.questiongroup_set.get(pk=questiongroup).question_set.get(pk=question)
    answer_set = question.answer_set.all()
    myData = {
        'labels': [strip_tags(a.answer_text) for a in answer_set],
        'series': [a.number_of_responses() for a in answer_set]
    }
    if room_is_owned_by_user(room_obj, request.user):
        return render(request, 'vote/question_response.html', {'room': room, 'questiongroup': questiongroup, 'question': question, 'data': myData})
    messages.error(request, 'You must own the room to see results')
    return redirect(room_obj)   # Default, return to room


@login_required
def answer_response(request, room, questiongroup, question):
    if not request.method == 'POST':
        return HttpResponse(403)

    subscription = user_is_subscribed(room, request.user)

    room_obj = get_object_or_404(Room, pk=room)
    qg = room_obj.questiongroup_set.get(pk=questiongroup)
    if subscription or room_obj.owner == request.user and qg.is_open:
        question_obj = qg.question_set.get(pk=question)
        if question_obj.is_open:
            if not request.POST.get('answer'):
                messages.error(request, 'You have to select one of the answers!')
                return redirect(question_obj)
            answer_obj = question_obj.answer_set.get(pk=request.POST['answer'])
            response, created = Response.objects.update_or_create(question=question_obj, user=request.user, defaults={'answer': answer_obj, 'user': request.user, 'question': question_obj})
            answer_set = question_obj.answer_set.all()
            myData = {
                'total_responses': question_obj.total_responses(),
                'labels': [a.answer_text for a in answer_set],
                'series': [a.number_of_responses() for a in answer_set]
            }
            event = "response-%s%s%s" % (room, questiongroup, question)
            get_pusher().trigger('crs', event, {'data': myData})
    return redirect(qg)


@login_required
def get_response_data(request, room, questiongroup, question):
    room_obj = get_object_or_404(Room, pk=room)
    question = room_obj.questiongroup_set.get(pk=questiongroup).question_set.get(pk=question)
    answer_set = question.answer_set.all()
    myData = {
        # 'question': question.question_text,
        'labels': [strip_tags(a.answer_text) for a in answer_set],
        'series': [a.number_of_responses() for a in answer_set]
    }

    return JsonResponse({'data': myData})


def user_is_subscribed(room, user):
    try:
        return Subscription.objects.get(room=room, user=user)
    except Subscription.DoesNotExist:
        return None
