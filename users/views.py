from users.models import Address, UserMobileNo
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User

from .forms import CreateUserForm, UpdateUserForm


def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('products:homepage')
        else:
            messages.info(request, 'Username or Password is incurrect ')

    content = {}
    return render(request, 'login.html', content)


def logout_page(request):
    logout(request)
    return redirect('users:login_user')


def register_page(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        print("methoad is post")
        if form.is_valid():
            print("form is valideted")
            form.save()
            return redirect('users:login_user')

    content = {'form': form}
    return render(request, 'register.html', content)


def user_profile(request):
    try:
        user_mobile_number = UserMobileNo.objects.filter(user = request.user.id)[0]
    except:
        user_mobile_number = None
    try:
        address = Address.objects.filter(user = request.user.id)[0]
    except:
        address = None

    context = {'user_mobile_number':user_mobile_number, 'address':address}
    return render(request, 'user_profile.html', context)


def edit_user_profile(request):
    user_form = UpdateUserForm()
    context = {'user_form':user_form}
    return render (request, 'user_profile_edit.html', context)