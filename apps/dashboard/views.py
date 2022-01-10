from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Sugar
from datetime import datetime


def main(request):
    if str(request.user) == 'AnonymousUser':
        user_logged = False
        ctx = {'user_logged': user_logged}
    else:
        user_logged = True
        username = request.user.username
        sugars = Sugar.objects.all().filter(user_id=request.user.id)
        index_list = []
        for i in sugars:
            i = str(i)
            index = i.split(',')[1]
            time = i.split(',')[3].split(':')[0:2]
            index_list.append(f'{time[0]}:{time[1]} - {index}')
        sugar_list = []
        ctx = {'user_logged': user_logged, 'username': username, 'sugar_list': sugar_list, 'index_list': index_list}
    return render(request, 'dashboard.html', ctx)


def info(request):
    if str(request.user) == 'AnonymousUser':
        user_logged = False
        ctx = {'user_logged': user_logged}
    else:
        if request.method == 'GET':
            user_logged = True
            username = request.user.username
            ctx = {'user_logged': user_logged, 'username': username}
    return render(request, 'info.html', ctx)


def add_sugar(request):
    if request.method == 'POST':
        index = request.POST['index']
        user = request.user.id
        dt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        Sugar(user_id=user, index=index, dt=dt).save()
        return redirect(reverse('dashboard:main'))
