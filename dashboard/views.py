from django.shortcuts import render, redirect


# Create your views here.
def dashboard(request):
    if request.user.is_authenticated():
        return render(request, 'dashboard/dashboard.html')
    else:
        # return render(request, 'authentication/login_form.html')
        return redirect('/authentication/login')
