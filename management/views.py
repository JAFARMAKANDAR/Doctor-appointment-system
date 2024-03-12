from django.shortcuts import render



# Create your views here.
def index(request):
       return render(request, 'index.html')

def Service(request):
       return render(request, 'service.html')


def About(request):
       return render(request, 'about.html')

def Register(request):
       return render(request, 'register.html')

def Login(request):
       return render(request, 'login.html')



