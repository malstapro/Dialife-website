from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Sugar
from datetime import datetime
import json


month_names = {'1': 'січня', '2': 'лютого', '3': 'березня', '4': 'квітня', '5': 'травня', '6': 'червня', '7': 'липня', '8': 'серпня', '9': 'вересня', '10': 'жовтня', '11': 'листопада', '12': 'грудня'}


def main(request):
    if str(request.user) == 'AnonymousUser':
        # If the user is not logged in
        user_logged = False
        ctx = {'user_logged': user_logged}
    else:
        # If the user is logged in
        user_logged = True
        username = request.user.username
        sugars = Sugar.objects.all().filter(user_id=request.user.id)
        index_list = []
        chart_data = {'time': [], 'indexes': []}
        for i in sugars:
            i = str(i)
            index = i.split(',')[1]
            date = i.split(',')[2]
            time = i.split(',')[3].split(':')[0:2]
            if date == str(datetime.now().date()):
                index_list.append(f'{time[0]}:{time[1]} - {index}')
                chart_data['time'].append(f'{time[0]}:{time[1]}')
                chart_data['indexes'].append(index)
        if len(index_list) == 0:
            index_list = ['Немає показників']
        today_date = f'{datetime.now().day} {month_names[str(datetime.now().month)]}'
        ctx = {'user_logged': user_logged, 'username': username, 'index_list': index_list, 'chart_data_time': chart_data['time'], 'chart_data_indexes': chart_data['indexes'], 'today_date': today_date}
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
