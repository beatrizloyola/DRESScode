from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

def landing_page(request):
    return render(request, 'Landing.html')

def login_page(request):
    return render(request, 'Login.html')

def signup_page(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            return render(request, 'SignUp.html', {'error': 'As senhas não coincidem. Tente novamente.'})
        
        if User.objects.filter(username=email).exists():
            return render(request, 'SignUp.html', {'error': 'Este e-mail já está cadastrado.'})

        user = User.objects.create_user(
            username=email, 
            email=email, 
            password=password,
            first_name=name
        )
        user.save()

        return redirect('login')

    return render(request, 'SignUp.html')

def login_page(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'Login.html', {'error': 'E-mail ou senha incorretos.'})

    return render(request, 'Login.html')

def dashboard_page(request):
    return render(request, 'Dashboard.html')