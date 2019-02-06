from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate
from django.contrib import auth
from django.contrib.auth.decorators import login_required

# Create your views here.

def login(request):
    if request.user.is_authenticated:
        return redirect(reverse('poker_index'))
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        if(username and password):
            user = authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect(reverse('poker_index'))
            else:
                message = "帳號或密碼錯誤"
        else:
            message = "請輸入所有的欄位"
    return render(request, 'user/login.html', locals())
    
def logout(request):
    auth.logout(request)
    return redirect(reverse('login'))