import django.core.exceptions
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate

from .forms import UpdateUserForm


def registerPage(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            redirect(reverse('dashboard:main'))
        else:
            print('form not valid')

    ctx = {'form': form}
    return render(request, 'register.html', ctx)


def loginPage(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        print(form.is_valid())
        print(form.cleaned_data)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                print(user)
                login(request, user)
                return redirect(f'/account?username={user.username}')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    form = AuthenticationForm()
    ctx = {'form': form}
    return render(request, 'login.html', ctx)


def account(request):
    if str(request.user) == 'AnonymousUser':
        user_logged = False
        ctx = {'user_logged': user_logged}
    else:
        if request.method == 'GET':
            user_form = UpdateUserForm(request, instance=request.user)
            user_logged = True
            username = request.user.username
            first_name = request.user.first_name
            last_name = request.user.last_name
            email = request.user.email
            ctx = {'form_valid': True, 'user_logged': user_logged, 'username': username, 'first_name': first_name, 'last_name': last_name, 'email': email, 'form': user_form}
        elif request.method == 'POST':
            username = request.POST['username']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            email = request.POST['email']
            user_form = UpdateUserForm(request.POST, instance=request.user)
            if user_form.is_valid():
                user_form.save()
                return redirect(reverse('dashboard:main'))
            else:
                user_logged = True
                ctx = {'form_valid': False, 'user_logged': user_logged, 'username': username, 'first_name': first_name, 'last_name': last_name, 'email': email, 'form': user_form}
        else:
            pass
    return render(request, 'account.html', ctx)


def updateUser(request):
    pass


def logoutPage(request):
    logout(request)
    return redirect('/')
