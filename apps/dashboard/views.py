from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Sugar
from datetime import datetime
import json


def main(request):
    if str(request.user) == 'AnonymousUser':
        user_logged = False
        ctx = {'user_logged': user_logged}
    else:
        user_logged = True
        username = request.user.username
        sugars = Sugar.objects.all().filter(user_id=request.user.id)
        index_list = []
        chart_data = {'time': [], 'indexes': []}
        for i in sugars:
            i = str(i)
            index = i.split(',')[1]
            time = i.split(',')[3].split(':')[0:2]
            index_list.append(f'{time[0]}:{time[1]} - {index}')
            chart_data['time'].append(f'{time[0]}:{time[1]}')
            chart_data['indexes'].append(index)
        ctx = {'user_logged': user_logged, 'username': username, 'index_list': index_list, 'chart_data_time': chart_data['time'], 'chart_data_indexes': chart_data['indexes']}
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
    with open('apps/dashboard/data/food_data.json', 'r') as json_file:
        data = json.load(json_file)
        food_list = data['data']
    ctx['food_list'] = food_list
    return render(request, 'info.html', ctx)


def add_sugar(request):
    if request.method == 'POST':
        index = request.POST['index']
        user = request.user.id
        dt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        Sugar(user_id=user, index=index, dt=dt).save()
        return redirect(reverse('dashboard:main'))
