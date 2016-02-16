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
