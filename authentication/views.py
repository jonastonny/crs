from django.shortcuts import render

# Create your views here.
from django.contrib.auth import views


def change_password(request):
    template_response = views.password_change(request)
    # Do something with `template_response`
    return template_response
