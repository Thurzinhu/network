from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from .forms import LoginForm

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
                    return HttpResponse('Success')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('invalid')    
    else:
        form = LoginForm()
    return render(request, 'account/login.html', { 'form': form })


@login_required
def dashboard(request):
    return render(request, 'account/dashboard.html', {'section': 'dashboard'})