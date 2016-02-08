from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

# Create your views here.
from django.views import generic

from django.views.generic import *


class IndexView(TemplateView):
    template_name = 'home/index.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect('dashboard')
        return render(request, self.template_name)


@login_required
def profile_detail(request):
    return render(request, template_name='home/profile_detail.html', context={'user': request.user})

