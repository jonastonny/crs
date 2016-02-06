from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.shortcuts import render, redirect
from . import forms
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm, PasswordChangeForm


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
    return render(request, "authentication/register.html", {'form': form, })


# def reset_password(request):
#     if request.method == 'POST':
#         form = PasswordResetForm(request.POST)
#         if form.is_valid():
#             form.save(request=request)
#             return redirect("done/")
#     else:
#         form = PasswordResetForm()
#         return render(request, "authentication/password_reset_form.html", {'form': form, })


# def reset_password_done(request):
#     return render(request, "authentication/password_reset_done.html")


# def reset_password_change(request, uidb64, token):
#     # if request.method == 'POST':
#     #     form = SetPasswordForm(user=request.user, data=request.POST)
#     #     if form.is_valid():
#     #         form.save()
#     #         update_session_auth_hash(request, form.user)
#     #         return redirect("complete/")
#     # else:
#         form = SetPasswordForm(user=request.user)
#         return render(request, "authentication/password_reset_confirm.html", {'form': form, })
