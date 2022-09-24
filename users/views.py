from users.models import Address, UserDetails, Plans, UserPlans
from products.models import *
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.encoding import force_bytes

from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

# from django_ecommerce import custom_decorators

from .forms import CreateUserForm, UserAddressForm
import uuid
import datetime


def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username +" : "+ password)
        try:
            user_details = UserDetails.objects.get(user_name = username)
            print(user_details)
            if user_details.verification == True:
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('products:homepage')
                else:
                    messages.info(request, 'Username or Password is incorrect ')
            
            elif user_details.verification == False:
                return render(request, 'login_email_verification.html', {'messages': ["Your email is not verified, Please resend the link and try again."], 'resend_email': True})
        except:
            return render(request, 'login.html', {"messages": ['Username is not registered']})

    content = {}
    return render(request, 'login.html', content)


def logout_page(request):
    logout(request)
    return redirect('users:login_user')


def verification(request, token):
    if request.user.is_authenticated:
        return redirect('products:homepage')
    if token:
        try:
            user_details = UserDetails.objects.get(verification_token=token)
            print(user_details)
            print("user_details.user_id: ", user_details.user_id)
            # user = User.objects.get(username=user_details.user_id)
            print(user_details.verification)
            decoded_token = str(urlsafe_base64_decode(token))
            print("decoded_token: ", decoded_token)
            if str(user_details.user_id) in decoded_token and user_details.verification == False:
                user_details.verification = True
                user_details.save()
                return render(request, 'login_email_verification.html', {'messages': ["Your Email is verified, Please login"]})
            elif user_details.verification == True:
                return render(request, 'login_email_verification.html', {'messages': ["Your Email is Already verified"]})
            else:
                return render(request, 'login_email_verification.html', {'messages': ["Your email is not verified, Please resend the link and try again."], 'resend_email': True})
        except:
            return render(request, 'resend_verification_email.html', {'messages': ["Token is expired please resend the token and try to verify your email."]})


def resend_verification(request):
    if request.user.is_authenticated:
        return redirect('products:homepage')

    if request.method == 'POST':
        email = request.POST.get('user_email')
        print(email)
        try:
            user = User.objects.get(email=email)
            if user:
                current_site = get_current_site(request)
                uid = str(uuid.uuid4()) + str(user.username)
                print("uid: ", uid)
                token = urlsafe_base64_encode(force_bytes(uid))
                verification_link = 'https://' + current_site.domain + '/user/verification/' + token + '/'
                user_details = UserDetails.objects.get(user_id=user)
                print("user details: ", user_details)
                user_details.verification_token = token
                user_details.save()

                # Send the email with new link
                subject = 'Thank you for registration, Please verify your email address'
                html_message = render_to_string('email_verification.html', {'verification_link': verification_link, 'username': user.username})
                plain_message = strip_tags(html_message)
                from_email = 'Django-eCommerce <pragnakalpdjango@gmail.com>'
                to = [user.email]

                # send_mail(subject, plain_message, from_email, to, html_message=html_message)

                return render(request, 'resend_verification_email.html', {'messages':['Email is send please check your inbox and also spam']})
        except:
            return render(request, 'resend_verification_email.html', {'messages':['Email is not registered']})

    return render(request, 'resend_verification_email.html')


def register_page(request):
    if request.user.is_authenticated:
        return redirect('products:homepage')

    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            print(request.POST)
            cleaned_data = form.cleaned_data
            cleaned_data['password'] = cleaned_data['password1']
            cleaned_data.pop('password1', None)
            cleaned_data.pop('password2', None)
            user = User(**cleaned_data)
            user.save()
            # form.save()
            context = form.cleaned_data
            user = User.objects.filter(username = context['username'], email = context['email'])[0]

            # Activate default plans for new users
            try:
                plan = Plans.objects.get(is_default = True)
                # print("PLANS DETAILS: ", plan)
                # print(plan.durations)
                activated_date = datetime.datetime.now()
                expire_date = activated_date + datetime.timedelta(days=int(int(plan.durations)*30.417))
                UserPlans.objects.create(user_id = user, plan=plan, price = plan.price, active = True, 
                                        activated_date = str(activated_date), expire_date = str(expire_date))
            except:
                pass
            # Create verifications link 
            current_site = get_current_site(request)
            uid = str(uuid.uuid4()) + str(context['username'])
            token = urlsafe_base64_encode(force_bytes(uid))
            verification_link = 'http://' + current_site.domain + '/user/verification/' + token + '/'
            UserDetails.objects.create(user_id=user, user_name=context['username'], verification=False, verification_token=token)

            # Send verification email notification
            subject = 'Thank you for registration, Please verify your email address'
            html_message = render_to_string('email_verification.html', {'verification_link': verification_link, 'username': context['username']})
            plain_message = strip_tags(html_message)
            from_email = 'Django-eCommerce <pragnakalpdjango@gmail.com>'
            to = [context['email']]

            send_mail(subject, plain_message, from_email, to, html_message=html_message)
            # return redirect('users:login_user')
            return render(request, 'login.html', {'messages': ["Email Verification Email Send Please verify your email and login."]})


    content = {'form': form}
    return render(request, 'register.html', content)


def plans(request):
    if request.user.is_authenticated:
        user_plan = UserPlans.objects.get(user_id = request.user.id, active=True)
        plans = Plans.objects.filter(active=True)
        user_plan.activated_date = user_plan.activated_date.date()
        user_plan.expire_date = user_plan.expire_date.date()
        # print(user_plan.activated_date)
        # print("DATE: ", user_plan.activated_date.date())
        # print(type(user_plan.activated_date))

        return render(request, 'available_plans.html', {'user_plan':user_plan, 'plans':plans, 'select':True})

    plan_details = Plans.objects.filter(active=True)
    plans = []    
    for plan in plan_details:
        plans.append(plan)
    return render(request, 'available_plans.html', {'user_plan':plans})


def update_plan(request):
    if request.method == 'POST':
        selected_plan = request.POST.get('plan')
        current_plan = UserPlans.objects.get(active=True, user_id = request.user.id)
        plan = Plans.objects.get(active=True, id=selected_plan)
        activated_date = datetime.datetime.now()
        expire_date = activated_date + datetime.timedelta(days=int(int(plan.durations)*30.417))
        current_plan.plan = plan
        current_plan.price = plan.price
        current_plan.activated_date = str(activated_date)
        current_plan.expire_date = str(expire_date)
        current_plan.active = True
        current_plan.save()

    return redirect('users:plans')


def user_profile(request):
    try:
        user_mobile_number = UserMobileNo.objects.filter(user = request.user.id)[0]
    except:
        user_mobile_number = None
    try:
        address = Address.objects.filter(user_id = request.user.id)[0]
    except:
        address = None

    context = {'user_mobile_number':user_mobile_number, 'address':address}
    return render(request, 'user_profile_dashbord.html', context)


def view_user_profile(request):
    context = {}
    return render(request, 'user_profile_display.html', context)


def edit_user_profile(request):
    # try to implement with multiple forms

    # mobile_form = UserMobileNo.objects.filter(user_id = request.user.id)
    # address_form = Address.objects.filter(user_id = request.user.id)
    

    # try:
    #     mobile = UserMobileNo.objects.filter(user_id = request.user.id)[0]
    # except:
    #     mobile = None
    # try:
    #     address = Address.objects.filter(user_id = request.user.id)[0]
    # except:
    #     address = None
        
    if request.method=='POST':  
        user = User.objects.filter(id = request.user.id)
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        user.update(first_name = first_name, last_name = last_name, username = username)

        # mobile_number = request.POST.get('mobile_number')
        # alternative_mobile_number = request.POST.get('alternative_mobile')

        # address_line_1 = request.POST.get('address_line_1')
        # address_line_2 = request.POST.get('address_line_2')
        # city = request.POST.get('city')
        # state = request.POST.get('state')
        # zip_code = request.POST.get('zipcode')
        # country = request.POST.get('country')

        # mobile = UserMobileNo.objects.filter(user_id = request.user.id)
        # # print("Length of mobile number data: ", len(mobile))
        # # print(mobile)
        # if len(mobile) >= 1:
        #     mob_obj = mobile.update(mobile_number = mobile_number, alternative_mobile_number = alternative_mobile_number)
        # else:
        #     mob_obj = UserMobileNo.objects.create(mobile_number = mobile_number, alternative_mobile_number = alternative_mobile_number, user_id = request.user.id)

        # address = Address.objects.filter(user_id = request.user.id)
        # # print("Length of mobile number data: ", len(mobile))
        # # print(mobile)
        # if len(address) >= 1:
        #     adr_obj = address.update(address_line_1 = address_line_1, address_line_2 = address_line_2, city = city, state = state, zip_code = zip_code, country = country)
        # else:
        #     adr_obj = Address.objects.create(address_line_1 = address_line_1, address_line_2 = address_line_2, city = city, state = state, zip_code = zip_code, country = country, user_id = request.user.id)

        return redirect('users:user_profile')

    context = {}
    return render (request, 'user_profile_edit.html', context)


def user_address(request):
    form = UserAddressForm()
    print('route called')
    if request.method == 'POST':
        form = UserAddressForm(request.POST)
        if form.is_valid():
            portfolio = form.save(commit=False)
            portfolio.user = request.user
            portfolio.save()
            return redirect('products:conformation')

    context = {'form': form}
    return render(request, 'user_address.html', context = context)


def order_history(request):
    orders = Orders.objects.filter(user_id=request.user)
    print(orders)
    for odr in orders:
        order_items = OrderItems.objects.filter(user_id=request.user.id, order_id=odr.id)
        odr.total_items = len(order_items)

    print(orders)

    context = {'orders': orders}

    return render(request, 'order_history.html', context = context)


def add_address(request):
    form = UserAddressForm()
    print('route called')
    if request.method == 'POST':
        form = UserAddressForm(request.POST)
        if form.is_valid():
            portfolio = form.save(commit=False)
            portfolio.user_id = request.user
            portfolio.save()
            return redirect('users:all_addresses')

    context = {'form': form}
    return render(request, 'user_address.html', context = context)


def select_address(request):
    address = Address.objects.filter(user_id = request.user.id)
    context = {'addresses': address}
    return render(request, 'select_address.html', context = context)

def all_addresses(request):
    addresses = Address.objects.filter(user_id=request.user.id)
    context = {'addresses': addresses}
    return render(request, 'all_addresses.html', context = context)


def edit_address(request, address_id):
    try:
        address = Address.objects.filter(pk=address_id, user_id = request.user.id)
        form = UserAddressForm(instance=address[0])
    except:
        return redirect('users:all_addresses')

    if request.method == 'POST':
        form = UserAddressForm(request.POST, instance=address[0])
        if form.is_valid():
            form.save()
            return redirect('users:user_profile')

    context = {'form': form}
    return render(request, 'edit_address.html', context = context)


def delete_address(request, address_id):
    try:
        Address.objects.filter(pk=address_id, user_id = request.user.id).delete()
    except:
        return redirect('users:all_addresses')
    
    return redirect('users:all_addresses')