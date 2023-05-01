from tkinter import FIRST
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
    #flags
    error = ""
    grd = ""
    #stores user details from request post sent from html file to variables
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
            #cretaes user object
            user_obj = User.objects.create_user(first_name=first, last_name=last, username=email, password=pwd)
            #creates employee object
            EmployeeUser.objects.create(user=user_obj, location=location, grade=grade, los=los, skills=skills, languages=languages)
            #no errors
            error = "no"
            #authenticates user
            user_obj=authenticate(username=email, password=pwd)
            #logs user in
            login(request,user_obj)
            #if statement to decide which home page user sees
            if grade in ["Associate", "Senior Associate", "Trainee"]:
                grd = "employee"
                redirect('associate_home')
            elif grade in ["Manager", "Senior Manager"]:
                grd="manager"
                redirect('manager_home')
            elif grade in ["Director", "Partner", "Resourcer"]:
                grd="resourcer"
                redirect('resourcer_home')
        except:
            error = "yes"
    #creates dictionary of data to send to html page
    d = {'error': error,
         'grd': grd}
    return render(request, "user_signup.html",d)

def loginFunc(request):
    error=""
    grd=""
    #gets email and password entered 
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        #authetnicates user
        user_obj = authenticate(username=email, password=password)
        if user_obj:
            user1 = EmployeeUser.objects.get(user=user_obj)
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
    #gets currently logged in users details
    currentUser = request.user
    employee = EmployeeUser.objects.get(user=currentUser)
    d = {'employee':employee}
    return render(request, "associate_home.html", d)

def manager_home(request):
    if not request.user.is_authenticated:
        return redirect('index')
    currentUser = request.user
    employee = EmployeeUser.objects.get(user=currentUser)
    d = {'employee':employee}
    return render(request, "manager_home.html",d)

def resourcer_home(request):
    if not request.user.is_authenticated:
        return redirect('index')
    currentUser = request.user
    employee = EmployeeUser.objects.get(user=currentUser)
    d = {'employee':employee}
    return render(request, "resourcer_home.html",d)

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
            #creates project role object using entries sent via post
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
    #queries datbase for project roles where the requester is the user logged in
    roles = ProjectRole.objects.filter(requester=userLoggedIn)
    d = {'roles':roles,
         'userGrade': userGrade}
    return render(request, "roles_listed.html", d)

def applicants(request, pid):
    if not request.user.is_authenticated:
        return redirect('loginFunc')
    userGrade=""
    user = request.user
    userLoggedIn = EmployeeUser.objects.get(user=user)
    grd = userLoggedIn.grade

    pRole = ProjectRole.objects.get(id=pid)
    if grd in ["Manager" , "Senior Manager"]:
        userGrade = "manager"
    else:
        userGrade = "resourcer"
    #queries to find applications that have the same project role as the one current user is viewing
    applicants = Applications.objects.filter(role=pRole)
    d = {'role':pRole,
         'userGrade': userGrade,
         'applicants': applicants}
    return render(request, "applicants.html", d)

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
    #queries database for project roles that have the same employee grade and line of service as currently logged in user
    roles = ProjectRole.objects.filter(grade=employee.grade, los=employee.los)
    d = {'roles':roles,
         'userGrade':userGrade}
    return render(request, "available_projects.html", d)

def role_desc(request, pid):
    error=""
    pRole = ProjectRole.objects.get(id=pid)
    user = request.user
    employee = EmployeeUser.objects.get(user=user)
    grd = employee.grade
    #splits skills fields into lists where there are commas
    roleSkills = list(pRole.skills.split(","))
    userSkills = list(employee.skills.split(","))
    #calculates the percentage of user skills present in role skills
    matchRating = (len(set(roleSkills).intersection(set(userSkills))))/len(roleSkills)*100
    if grd in ["Manager", "Senior Manager"]:
        userGrade = "manager"
    else:
        userGrade="employee"

    if request.method=="POST":
        try:
            #creates application object when the user applies
            Applications.objects.create(role=pRole, applicant=employee, applicationDate=date.today(), matchRating=matchRating)
            error="no"
        except:
            error="yes"
    d = {'pRole':pRole,
         'userGrade':userGrade,
         'error':error,
         'matchRating': matchRating}
    return render(request, 'role_desc.html', d)

def user_profile(request, uid):
    user = request.user
    employee = EmployeeUser.objects.get(user=user)
    grd = employee.grade
    if grd in ["Manager", "Senior Manager"]:
        userGrade = "manager"
    else:
        userGrade="resourcer"
    #queries for selected application
    application = Applications.objects.get(id=uid)
    #queries for selected uer
    userSelected = EmployeeUser.objects.get(id=application.applicant_id)
    matchRating = application.matchRating
    d = {'userSelected':userSelected,
         'userGrade':userGrade,
         'matchRating':matchRating
         }
    return render(request, 'user_profile.html', d)

def edit_profile(request):
    error=""
    user = request.user
    employee = EmployeeUser.objects.get(user=user)
    grd = employee.grade
    if grd in ["Manager", "Senior Manager"]:
        userGrade = "manager"
    elif grd in ["Associate", "Senior Associate", "Trainee"]:
        userGrade = "employee"
    else:
        userGrade="resourcer"
    if request.method=="POST":
        location = request.POST['location']
        grade = request.POST['grade']
        los = request.POST['los']
        skills = request.POST['skills']
        languages = request.POST['languages']
        try:
            #tries to update fields given the variables storing the input from the user
            employee.location=location
            employee.grade=grade
            employee.los=los
            employee.skills=skills
            employee.languages=languages

            employee.save()
            error="no"
        except:
            error="yes"

    d = {'userGrade':userGrade,
         'employee':employee,
         'error':error
         }
    return render(request, 'edit_profile.html', d)

def Logout(request):
    #logs out user
    logout(request)
    return redirect("index")
