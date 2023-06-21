import re
import django
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.models import User
from todo_app.models import Task
from .token import TokenGenerator
from todo_app.forms import TaskForm
from django.contrib import messages
from todo_app.forms import LoginForm
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from todo_app.forms import CustomRegistrationForm 
from django.contrib.auth.hashers import check_password
from django.utils.encoding import force_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site  
from django.contrib.auth import login, logout
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.template import Template
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.contrib.auth.forms import PasswordChangeForm 





User = get_user_model()

def send_registration_email(current_site,user_email, user):
    
    token = TokenGenerator().make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))  
    url = f"http://{current_site}/activate/{uid}/{token}"
    subject = 'Registration Confirmation'
    message = f'Thank you for registering with our website.{url}'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user_email]
    send_mail(subject, message, from_email, recipient_list)


def register(request):
    if request.method == "POST":
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            current_site = get_current_site(request)
            user_email = form.cleaned_data.get("email")
            send_registration_email(current_site, user_email, user)
            return redirect("login")
    else:
        form = CustomRegistrationForm()
    return render(request, "register.html", {"form": form})


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        try:
            user = User.objects.get(email=email)
            if check_password(password, user.password):
                
                login(request, user)
                  
                tasks = Task.objects.filter(user=user).order_by('due_date')
                # tasks = Task.objects.order_by('due_date')
                form = TaskForm()
                return render(request, 'task_list.html', {'tasks': tasks,'form': form})
            else:
                
                error_message = 'Invalid password'
                return render(request, 'login.html', {'error_message': error_message})
        
        except User.DoesNotExist:

            error_message = 'Invalid email'
            return render(request, 'login.html', {'error_message': error_message})
    
    return render(request, 'login.html')



def activate(request, uidb64, token):  
    User = get_user_model()  
    try:  
        uid = force_str(urlsafe_base64_decode(uidb64))  
        user = User.objects.get(pk=uid)  
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):  
        user = None  
    if user is not None and TokenGenerator.check_token(user, token):  
        user.is_active = True  
        user.save()  
        return redirect('login')  
    else:  
        return redirect('register')


def logout_view(request):
    logout(request)
    return redirect('login')



def forgot_password(request):
    
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None

        if user:
            token = default_token_generator.make_token(user)
            uid = user.pk
            current_site = get_current_site(request)
            mail_subject = 'Reset your password'
            reset_password_link = f"{current_site}/user/reset-password/{uid}/{token}        "
            
            print("Token---->",token)
            print("Uid----->",uid)
            print("currentsite----->",current_site)
            print("Password link----->",reset_password_link)
            
            context = dict(
                user = user,
                reset_password_link = reset_password_link,
            )
            message = render_to_string('reset_temp_email.html', 
                context
            )
            email = EmailMessage(mail_subject, message, to=[email])
            email.content_subtype = 'html' 
            email.send()
            
            # return redirect(reverse('password_reset_done', kwargs={'uid': uid, 'token': token}))
            return render(request, 'forgot_password.html')
    return render(request, 'forgot_password.html')

def reset_password(request, uid, token):
    user = get_object_or_404(User, pk=uid)
    if default_token_generator.check_token(user, token):
        if request.method == 'POST':
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')
            print("Password---> ",password)
            print("C_Password---> ",confirm_password)
            if password == confirm_password:
                print("CORRECT----->")
                user.set_password(password)
                print("CORRECT----->")
                user.save()
                return redirect('login')
            else:
                return HttpResponse('Passwords do not match')
        return render(request, 'reset_password.html')
    else:
        return HttpResponse('Invalid token')

def change_password(request):
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        # Check if the current password matches the user's actual password
        if not check_password(current_password, request.user.password):
            messages.error(request, 'Current password is incorrect.')

        # Check if the new password and confirm password match
        if new_password != confirm_password:
            messages.error(request, 'New password and confirm password do not match.')
            
            return render(request, 'change_password.html')

        # Update the user's password
        request.user.set_password(new_password)
        request.user.save()
        success = 'Your password has been changed successfully.'
        return render(request, 'login.html',{'success': success})    
        
def profile(request):
    context = {
        "username" : request.user.username,
        "first_name" : request.user.first_name,
        "last_name" : request.user.last_name,
        "address" : request.user.address,
        "pincode" : request.user.pincode,
        "email" : request.user.email,
        "mobile" : request.user.mobile,

    }
    if request.method == "POST":
        user = User.objects.get(pk = request.user.pk)  
        user.first_name = request.POST.get("first_name")
        user.last_name = request.POST.get("last_name")
        user.address = request.POST.get("address")
        user.mobile =request.POST.get("mobile") 
        user.pincode =request.POST.get("pincode") 
        user.save()  
        return redirect('profile')
    
    return render(request,'profile.html',context)




    