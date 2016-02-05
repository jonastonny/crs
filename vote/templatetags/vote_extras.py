from django import template

register = template.Library()

@register.filter
def room_is_owned_by_user(room, user_id):
    return room.id == user_id
