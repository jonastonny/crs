from django.shortcuts import render, redirect
from django.views import generic
from django.forms import EmailField
from django.contrib.auth.models import User

from django.utils.translation import ugettext_lazy as _

from django import forms
from django.contrib.auth.forms import UserCreationForm


# Create your views here.
# def register(request):
#     if request.user.is_authenticated():
#         return render(request, 'dashboard/dashboard.html')
#     else:
#         return render(request, 'authentication/register.html')


class UserCreationForm(UserCreationForm):
    email = EmailField(label=_("Email address"), required=True, help_text=_("Required."))

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return redirect("/dashboard/")
    else:
        form = UserCreationForm()
    return render(request, "authentication/register.html", {
        'form': form,
    })
