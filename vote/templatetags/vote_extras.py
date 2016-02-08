from django import template

register = template.Library()


@register.filter
def room_is_owned_by_user(room, user):
    return int(room.owner_id) == int(user.id)


@register.filter
def user_is_subscribed_to_room(user, room):
    return len(user.subscription_set.filter(room_id__in=str(room.id))) > 0
