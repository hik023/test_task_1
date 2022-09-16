from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import RegisterForm, LoginForm
from client.utils.helpers import create_user_api_session
from client.utils.exceptions import BadAPIAccess


def register_view(request):
    if request.user.is_authenticated:
        return redirect('client:home')
    if request.method == 'GET':
        form = LoginForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            try:
                create_user_api_session(user)
            except BadAPIAccess as e:
                return render(request, 'error_page.html', {'error': e.message})
            login(request, user)
            messages.success(request, 'Registration successful.' )
            return redirect('client:home')
        messages.error(request, 'Unsuccessful registration. Invalid information.')
  
    return render(request, 'registration/register.html', {'register_form':form})


def login_view(request):
    data = {}
    if request.method == 'GET':
        form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            
            user = authenticate(request, username=cd['username'], password=cd['password'])
            print(user)
            if user is not None:
                login(request, user)
                return redirect('client:home')
            data['error'] = 'Логин или пароль неверный!'
    data['form'] = form
    return render(request, 'registration/login.html', data)


@login_required
def logout_view(request):
    logout(request)
    return redirect('client:home')