from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from .models import Post, LikePost, Profile, Followers
from django.contrib.auth.models import User

from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegisterForm  # Import your custom form

def signup(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully!")
            return redirect('login')
        else:
            # If the form is invalid, show errors to the user
            return render(request, 'signup.html', {'form': form})
    else:
        form = RegisterForm()  # Initialize the form on GET request
    return render(request, 'signup.html', {'form': form})

def login(request):
    if request.method == 'POST':
        username = request.POST.get('fnm')
        password = request.POST.get('pwd')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('/')
        else:
            return render(request, 'login.html', {'invalid': 'Invalid Credentials'})
    return render(request, 'login.html')
