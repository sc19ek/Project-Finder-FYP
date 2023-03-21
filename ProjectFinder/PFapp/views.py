from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_protect
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout

# Create your views here.

def index(request):
    return render(request, "index.html")

def associate_login(request):
    error=""
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(username=email, password=password)
        if user:
            print(user)
            try:
                user1 = EmployeeUser.objects.get(user=user)
                print(user1)
                if user1.grade == "Associate":
                    print(user1)
                    login(request,user)
                    error="no"
                else:
                    error="yes"
            except:
                error="yes"
        else:
            error="yes"
    d = {'error':error}
    return render(request, "associate_login.html", d)

def Logout(request):
    logout(request)
    return redirect("index")