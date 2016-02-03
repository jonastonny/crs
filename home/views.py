from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.

from django.views.generic import *


class IndexView(TemplateView):
    template_name = 'home/index.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


