from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
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
    page = request.GET.get('page')
    rooms_list = Room.objects.filter(title__icontains=query)
    paginator = Paginator(rooms_list, 2)

    try:
        rooms = paginator.page(page)
    except PageNotAnInteger:
        rooms = paginator.page(1)
    except EmptyPage:
        rooms = paginator.page(paginator.num_pages)
    return render(request, template_name='dashboard/search_detail.html', context={'rooms': rooms, 'query': query})
