from users.models import Address, UserMobileNo
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User

from .forms import CreateUserForm


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
        if form.is_valid():
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
    try:
        mobile = UserMobileNo.objects.filter(user_id = request.user.id)[0]
    except:
        mobile = None
    try:
        address = Address.objects.filter(user_id = request.user.id)[0]
    except:
        address = None
        
    if request.method=='POST':  
        user = User.objects.filter(id = request.user.id)
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        user.update(first_name = first_name, last_name = last_name, username = username)

        mobile_number = request.POST.get('mobile_number')
        alternative_mobile_number = request.POST.get('alternative_mobile')

        address_line_1 = request.POST.get('address_line_1')
        address_line_2 = request.POST.get('address_line_2')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip_code = request.POST.get('zipcode')
        country = request.POST.get('country')

        try:
            mobile = UserMobileNo.objects.filter(user_id = request.user.id)
            mobile.update(mobile_number = mobile_number, alternative_mobile_number = alternative_mobile_number)
        except:
            UserMobileNo.objects.create(mobile_number = mobile_number, alternative_mobile_number = alternative_mobile_number, user_id = request.user.id)

        try:
            address = Address.objects.filter(user_id = request.user.id)
            address.update(address_line_1 = address_line_1, address_line_2 = address_line_2, city = city, state = state, zip_code = zip_code, country = country)
        except:
            Address.objects.create(address_line_1 = address_line_1, address_line_2 = address_line_2, city = city, state = state, zip_code = zip_code, country = country, user_id = request.user.id)

        return redirect('users:user_profile')

    context = {'mobile':mobile, 'address':address}
    return render (request, 'user_profile_edit.html', context)