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
            return redirect(reverse('account:login'))
        else:
            form_valid = False
            ctx = {'form': form, 'form_valid': form_valid}
            return render(request, 'register.html', ctx)
    else:
        ctx = {'form': form, 'form_valid': True}
        return render(request, 'register.html', ctx)


def loginPage(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            form_valid = True
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                print(user)
                login(request, user)
                return redirect(reverse('dashboard:main'))
            else:
                form_valid = False
        else:
            form_valid = False
        ctx = {'form': form, 'form_valid': form_valid}
        return render(request, 'login.html', ctx)
    else:
        form = AuthenticationForm()
        ctx = {'form': form, 'form_valid': True}
        return render(request, 'login.html', ctx)


def account(request):
    if str(request.user) == 'AnonymousUser':
        # If the user is not logged in
        user_logged = False
        ctx = {'user_logged': user_logged}
    else:
        # If the user is logged in
        if request.method == 'GET':
            # Generate page
            user_form = UpdateUserForm(request, instance=request.user)
            user_logged = True
            username = request.user.username
            first_name = request.user.first_name
            last_name = request.user.last_name
            email = request.user.email
            ctx = {'form_valid': True, 'user_logged': user_logged, 'username': username, 'first_name': first_name, 'last_name': last_name, 'email': email, 'form': user_form}
        elif request.method == 'POST':
            # On form submit
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


def logoutPage(request):
    logout(request)
    return redirect('/')
