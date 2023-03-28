from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_protect
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout

# Create your views here.

def index(request):
    return render(request, "index.html")

def user_signup(request):
    error = ""
    if request.method=="POST":
        first = request.POST['firstName']
        last = request.POST['lastName']
        email = request.POST['email']
        location = request.POST['location']
        grade = request.POST['grade']
        los = request.POST['los']
        skills = request.POST['skills']
        languages = request.POST['languages']
        pwd = request.POST['password']
        try:
            user = User.objects.create_user(first_name=first, last_name=last, username=email, password=pwd)
            EmployeeUser.objects.create(user=user, location=location, grade=grade, los=los, skills=skills, languages=languages)
            error = "no"
        except:
            error = "yes"
    d = {'error': error}
    return render(request, "user_signup.html",d)

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

def resourcer_login(request):
    error=""
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(username=email, password=password)
        if user:
            try:
                user1 = EmployeeUser.objects.get(user=user)
                print(user1)
                if user1.grade == "Resourcer":
                    login(request,user)
                    error="no"
                else:
                    error="yes"
            except:
                error="yes"
        else:
            error="yes"
    print(error)
    d = {'error':error}
    return render(request, "resourcer_login.html", d)

def associate_home(request):
    if not request.user.is_authenticated:
        return redirect('index')
    return render(request, "associate_home.html")

def resourcer_home(request):
    if not request.user.is_authenticated:
        return redirect('index')
    return render(request, "resourcer_home.html")

def add_project(request):
    if not request.user.is_authenticated:
        return redirect('resourcer_login')
    error = ""
    if request.method=="POST":
        pTitle = request.POST['projectTitle']
        rTitle = request.POST['roleTitle']
        loc = request.POST['location']
        grd = request.POST['grade']
        sDate = request.POST['startDate']
        eDate = request.POST['endDate']
        desc = request.POST['description']
        skills = request.POST['skills']
        currentUser = request.user
        requester = EmployeeUser.objects.get(user=currentUser)
        try:
            ProjectRole.objects.create(requester=requester, projectTitle=pTitle, roleTitle=rTitle, grade=grd, startDate=sDate, 
                                              endDate=eDate, description=desc, skills=skills, baseOffice=loc, creationDate=date.today())
            error = "no"
        except:
            error = "yes"
    d = {'error': error}
    return render(request, "add_project.html", d)

def roles_listed(request):
    if not request.user.is_authenticated:
        return redirect('resourcer_login')
    user = request.user
    resourcer = EmployeeUser.objects.get(user=user)
    roles = ProjectRole.objects.filter(requester=resourcer)
    d = {'roles':roles}
    return render(request, "roles_listed.html", d)

def available_projects(request):
    if not request.user.is_authenticated:
        return redirect('index')
    user = request.user
    employee = EmployeeUser.objects.get(user=user)
    roles = ProjectRole.objects.filter(grade=employee.grade)
    d = {'roles':roles}
    return render(request, "available_projects.html", d)

def Logout(request):
    logout(request)
    return redirect("index")
