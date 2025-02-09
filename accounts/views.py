from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login,logout as auth_logout  # Import Django's built-in login function
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegistrationForm
from django.contrib.auth.models import User


def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])  # Hash password
            user.save()
            return redirect("accounts:login")  # Redirect to login page after successful signup
    else:
        form = RegistrationForm()

    return render(request, "register.html", {"form": form})

def login(request):  # Keeping the name "login"
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)  # Use Django's login function with the alias
            return redirect('videos:index')  # Redirect to home page after login
    else:
        form = AuthenticationForm()
    
    return render(request, 'login.html', {'form': form})

def logout(request):
    auth_logout(request)
    return redirect("accounts:login")

