from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib import messages
from .forms import (
    LoginForm,
    UserRegistrationForm,
    UserEditForm,
    ProfileEditForm
)
from .models import Profile


def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # hash user password
            user.set_password(form.cleaned_data["password"])
            user.save()
            Profile.objects.create(user=user)
            return render(
                request,
                "account/register_done.html",
                {"new_user": user}
            )
    else:
        form = UserRegistrationForm()
    return render(
        request,
        "account/register.html",
        {"form": form}
    )


def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse("Success")
                else:
                    return HttpResponse("Disabled account")
            else:
                return HttpResponse("invalid")    
    else:
        form = LoginForm()
    return render(request, "account/login.html", { "form": form })


@login_required
def dashboard(request):
    return render(request, "account/dashboard.html", {"section": "dashboard"})


@login_required
def edit(request):
    if request.method == "POST":
        user_form = UserEditForm(
            instance=request.user,
            data=request.POST
        )
        profile_form = ProfileEditForm(
            instance=request.user.profile,
            data=request.POST,
            files=request.FILES
        )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(
                request,
                "Profile updated successfully"
            )
        else:
            messages.error(
                request,
                "Error updating your profile"
            )
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(
        request,
        "account/edit.html",
        {
            "user_form": user_form,
            "profile_form": profile_form
        }
    )