from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from . import forms


def register(request):
    if request.method == 'POST':
        form = forms.CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(username=request.POST['username'], password=request.POST['password1'])
            login(request, user)
            return redirect("/dashboard/")
    else:
        form = forms.CustomUserCreationForm()
    return render(request, "authentication/register.html", {'form': form})
