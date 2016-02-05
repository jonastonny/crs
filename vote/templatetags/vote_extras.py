from django import template

register = template.Library()

@register.filter
def room_is_owned_by_user(room, user):
    return int(room.owner_id) == int(user.id)
