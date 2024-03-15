from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


# Create your views here.
def index(request):
       if not request.user.is_staff:
              return redirect('login')
       return render(request, 'index.html')

def Service(request):
       return render(request, 'service.html')


def About(request):
       return render(request, 'about.html')

def Register(request):
       return render(request, 'register.html')

def Login(request):
    error = ""
    if request.method == 'POST':
        u = request.POST['uname']
        p = request.POST['pwd']
        user = authenticate(username=u, password=p)
        if user is not None:
            if user.is_staff:
                login(request, user)
                return redirect('home')
            else:
                error = "Invalid credentials"
        else:
            error = "Invalid credentials"

    return render(request, 'login.html', {'error': error})

def Logout_admin(request):
    if not request.user.is_staff:
        return redirect('login')
    logout(request)
    return redirect('login')


