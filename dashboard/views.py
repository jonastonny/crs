from django.http import HttpResponse
from django.views import generic

from vote.models import Room
from django.shortcuts import render, redirect


# Create your views here.


def dashboard(request):
    if request.user.is_authenticated():
        return render(request, 'dashboard/dashboard.html')
    else:
        return redirect('/authentication/login')


def searchRoom(request):
    query = request.GET.get('q', '')
    rooms = Room.objects.filter(title__icontains=query)
    return render(request, template_name='dashboard/search_detail.html', context={'rooms': rooms, 'query': query})
