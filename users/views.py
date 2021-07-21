from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from .forms import CreateUserForm

def home_page(request):
    return render(request, 'index.html')


def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            return redirect('homepage')
        else:
            messages.info(request, 'Username or Password is incurrect ')

    content = {}
    return render (request, 'login.html', content)  

def logout_page(request):
    logout(request)
    return redirect('/login/')

def register_page(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        print("methoad is post")
        if form.is_valid():
            print("form is valideted")
            form.save()
            return redirect('/login/')
    content = {'form':form}
    return render (request, 'register.html', content)  