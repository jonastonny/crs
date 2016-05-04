import short_url
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.views import generic
from django.views.decorators.cache import cache_page

from django.views.generic import *

from home.forms import HomeProfileEdit
from vote.models import QuestionGroup


class IndexView(TemplateView):
    template_name = 'home/index.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect('dashboard')
        return render(request, self.template_name)


@login_required
@cache_page(15)
def profile_detail(request):
    return render(request, template_name='home/profile_detail.html', context={'user': request.user})


@login_required
def profile_edit(request):
    user = request.user
    form = HomeProfileEdit(instance=user)
    context = {'user': user, 'form': form}
    return render(request, template_name='home/profile_edit.html', context=context)


@login_required
def profile_update(request):
    if not request.method == 'POST':
        return HttpResponse(status=201)
    user = request.user
    form = HomeProfileEdit(request.POST or None, instance=user)

    if form.is_valid():
        form.save()
        return redirect('profile')
    return render(request, 'home/profile_edit.html', {'user': user, 'form': form})


@login_required
def url_redirect(request, short):
    group_id = short_url.decode_url(short)
    group = get_object_or_404(QuestionGroup, pk=group_id)
    return redirect(group)