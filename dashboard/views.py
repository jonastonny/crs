from django.shortcuts import render

from django.http import HttpResponse


# Create your views here.
def dashboard(request):
    # if request.user.is_authenticated():
    #     return HttpResponse("Hello, you are logged in.")
    # else:
    #     return HttpResponse("NOT LOGGED IN")

    return render(request, 'dashboard/dashboard.html')
