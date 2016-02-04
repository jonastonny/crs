from django.shortcuts import render, redirect
from . import forms
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm, PasswordChangeForm


def register(request):
    if request.method == 'POST':
        form = forms.CustomUserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return redirect("/dashboard/")
    else:
        form = forms.CustomUserCreationForm()
    return render(request, "authentication/register.html", {'form': form, })


def reset_password(request):
    form = PasswordResetForm()
    return render(request, "authentication/password_reset_form.html", {'form': form, })


def reset_password_done(request):

    return render(request, "authentication/password_reset_done.html")
