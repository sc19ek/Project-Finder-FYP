from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_protect
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from datetime import date

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
            user_obj = User.objects.create_user(first_name=first, last_name=last, username=email, password=pwd)
            EmployeeUser.objects.create(user=user_obj, location=location, grade=grade, los=los, skills=skills, languages=languages)
            error = "no"
        except:
            error = "yes"
    d = {'error': error}
    return render(request, "user_signup.html",d)

def loginFunc(request):
    error=""
    grd=""
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user_obj = authenticate(username=email, password=password)
        print(user_obj)
        if user_obj:
            user1 = EmployeeUser.objects.get(user=user_obj)
            print(user1)
            login(request,user_obj)
            if user1.grade in ["Associate", "Senior Associate", "Trainee"]:
                error="no"
                grd="employee"
            elif user1.grade in ["Manager", "Senior Manager"]:
                error="no"
                grd="manager"
            elif user1.grade in ["Director", "Partner", "Resourcer"]:
                error="no"
                grd="requester"
            else:
                error="yes"
        else:
            error="yes"
    d = {'error':error,
         'grd':grd}
    print(d)
    return render(request, "loginFunc.html", d)

def associate_home(request):
    if not request.user.is_authenticated:
        return redirect('index')
    return render(request, "associate_home.html")

def manager_home(request):
    if not request.user.is_authenticated:
        return redirect('index')
    return render(request, "manager_home.html")

def resourcer_home(request):
    if not request.user.is_authenticated:
        return redirect('index')
    return render(request, "resourcer_home.html")

def add_project(request):
    if not request.user.is_authenticated:
        return redirect('loginFunc')
    error = ""
    currentUser = request.user
    requester = EmployeeUser.objects.get(user=currentUser)
    grd = requester.grade
    if grd in ["Manager" , "Senior Manager"]:
        userGrade = "manager"
    else:
        userGrade = "resourcer"
    if request.method=="POST":
        pTitle = request.POST['projectTitle']
        rTitle = request.POST['roleTitle']
        los = request.POST['los']
        loc = request.POST['location']
        grd = request.POST['grade']
        sDate = request.POST['startDate']
        eDate = request.POST['endDate']
        desc = request.POST['description']
        skills = request.POST['skills']
        try:
            ProjectRole.objects.create(requester=requester, projectTitle=pTitle, roleTitle=rTitle, los=los, grade=grd, startDate=sDate, 
                                   endDate=eDate, description=desc, skills=skills, baseOffice=loc, creationDate=date.today())
            error="no"
        except:
            error="yes"

    d = {'error':error,
         'userGrade': userGrade}
    return render(request, "add_project.html", d)

def roles_listed(request):
    if not request.user.is_authenticated:
        return redirect('loginFunc')
    userGrade=""
    user = request.user
    userLoggedIn = EmployeeUser.objects.get(user=user)
    grd = userLoggedIn.grade
    if grd in ["Manager" , "Senior Manager"]:
        userGrade = "manager"
    else:
        userGrade = "resourcer"
    roles = ProjectRole.objects.filter(requester=userLoggedIn)
    d = {'roles':roles,
         'userGrade': userGrade}
    return render(request, "roles_listed.html", d)

def available_projects(request):
    if not request.user.is_authenticated:
        return redirect('loginFunc')
    user = request.user
    employee = EmployeeUser.objects.get(user=user)
    grd = employee.grade
    if grd in ["Manager", "Senior Manager"]:
        userGrade = "manager"
    else:
        userGrade="employee"
    roles = ProjectRole.objects.filter(grade=employee.grade)
    d = {'roles':roles,
         'userGrade':userGrade}
    return render(request, "available_projects.html", d)

def role_desc(request, pid):
    error=""
    pRole = ProjectRole.objects.get(id=pid)
    user = request.user
    employee = EmployeeUser.objects.get(user=user)
    grd = employee.grade
    if grd in ["Manager", "Senior Manager"]:
        userGrade = "manager"
    else:
        userGrade="employee"

    if request.method=="POST":
        try:
            Applications.objects.create(role=pRole, applicant=employee, applicationDate=date.today())
            error="no"
        except:
            error="yes"
    d = {'pRole':pRole,
         'userGrade':userGrade,
         'error':error}
    return render(request, 'role_desc.html', d)


def Logout(request):
    logout(request)
    return redirect("index")
