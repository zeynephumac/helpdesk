from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import User


       
# login a user
def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
            if user.check_password(password) and user.is_active:
                user.login_attempts = 0
                user.save()
                login(request, user)
                messages.info(request, 'Login successfull')
                return redirect('dashboard')
            else:
                user.login_attempts += 1
                user.save()
                if user.login_attempts >= 3:
                    user.is_active = False
                    user.save()
                    messages.warning(request, 'Your account has been locked. Please contact a manager.')
                else:
                    messages.warning(request, 'Something went wrong. Please check form input')
                return redirect('login')
        except User.DoesNotExist:
            messages.warning(request, 'User not found')
            return redirect('login')
        
    else:
        return render(request, 'users/login.html')




# logout a user
def logout_user(request):
    logout(request)
    messages.info(request, 'Your session has ended. Please log in to continue')
    return redirect('login')



