from django import template

from vote.models import Room

register = template.Library()


@register.filter
def room_is_owned_by_user(room, user):
    return int(room.owner_id) == int(user.id)


@register.filter
def questiongroup_is_owned_by_user(questiongroup, user):
    room_obj = Room.objects.get(id=questiongroup.room_id)
    return int(room_obj.owner_id) == int(user.id)


@register.filter
def user_is_subscribed_to_room(user, room):
    return len(user.subscription_set.filter(room_id=str(room.id))) > 0


@register.filter
def group_disabled_class(questiongroup):
    if not questiongroup.is_open:
        return 'danger'


@register.filter
def answer_correct(answer):
    if answer.correct:
        return 'checked'


@register.filter
def what_did_user_answer(question, user):
    if not question.is_open:
        for answer in question.answer_set.all():
            for response in answer.response_set.all():
                if response.user_id == user.id:
                    if answer.correct:
                        return '<span class="glyphicon glyphicon-ok" aria-hidden="true"></span>'
                    else:
                        return '<span class="glyphicon glyphicon-remove" aria-hidden="true"></span>'
            # else:
            #     for response in answer.response_set.all():
            #         if response.user_id == user.id:
        return "Not registered"
    else:
        for answer in question.answer_set.all():
            for response in answer.response_set.all():
                if response.user_id == user.id:
                    return "Registered"
        return "Answer now!"


@register.filter
def get_letter(integer):
    return chr(ord('A') + integer)
