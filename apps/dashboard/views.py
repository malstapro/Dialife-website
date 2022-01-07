from django.shortcuts import render

def main(request):
    if str(request.user) == 'AnonymousUser':
        user_logged = False
        ctx = {'user_logged': user_logged}
    else:
        if request.method == 'GET':
            user_logged = True
            ctx = {'user_logged': user_logged}
    return render(request, 'dashboard.html', ctx)

def info(request):
    return render(request, 'info.html')
