from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate


def registerPage(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()

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
            user_logged = True
            username = request.GET['username']
            ctx = {'user_logged': user_logged, 'username': username}
        else:
            pass
    return render(request, 'account.html', ctx)


def logoutPage(requst):
    logout(requst)
    return redirect('/')
