from django.shortcuts import render, redirect
from .models import Member
from .forms import MemberForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout



def index(request):
    all_members = Member.objects.all
    return render(request, 'index.html', {'all':all_members})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ('You have been logged in '))
            return redirect('index')
        else:
            messages.success(request, ('There was an error loggin in please try again !!'))
            return redirect('login')
        

    else:
        return render(request, 'login.html', {})

def signup(request):
    if request.method == "POST":
        form = MemberForm(request.POST or None)
        if form.is_valid(): 
            form.save()
            messages.success(request, ('You Form been Submitted Seccessfuly'))
            return redirect('login')
        else:
            uname = request.POST['uname']
            email = request.POST['email']
            passwd = request.POST['passwd']
            repasswd = request.POST['repasswd']
            messages.success(request, ('There was an error in your form please try again '))
            return render(request, 'signup.html', {'uname':uname, 'email':email, 'passwd':passwd, 'repasswd':repasswd })
    
    else:
        return render(request, 'signup.html', {})

