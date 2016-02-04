from django.shortcuts import render, redirect
from . import forms


def register(request):
    if request.method == 'POST':
        form = forms.CustomUserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return redirect("/dashboard/")
    else:
        form = forms.CustomUserCreationForm()
    return render(request, "authentication/register.html", {
        'form': form,
    })
