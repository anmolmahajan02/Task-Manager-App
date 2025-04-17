from django.shortcuts import render,redirect,get_object_or_404
from .models import task
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
import threading

def email(regEmail,regUsername):
    send_mail(
                subject="Welcome to TaskManager!",
                message=f"Hi {regUsername},\n\nThanks for registering at TaskManager!",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[regEmail],
                fail_silently=False,
                )
# Create your views here.
def register(request):
    if request.method == 'POST':
        regUsername = request.POST['regUsername']
        regPassword = request.POST['regPassword']
        confirmPassword = request.POST['confirmPassword']
        regEmail = request.POST['regEmail']

        if regPassword == confirmPassword:
            if User.objects.filter(username = regUsername).exists():
                messages.info(request,"Username already exists")
                return redirect('register')
            else:
                registerUser = User.objects.create_user(username=regUsername, password=regPassword)
                registerUser.save()
                
                email_thread = threading.Thread(target=email, args=(regEmail, regUsername))
                email_thread.start()
        
                return redirect('login')
        else:
            messages.info(request,"Password doesnot match")
            return redirect("register")
    
    else:
        return render(request,'register.html')
                  
def login(request):
    if request.method ==  'POST':
        loginUsername = request.POST['loginUsername']
        loginPassword = request.POST['loginPassword']

        user = auth.authenticate(username = loginUsername,password = loginPassword)

        if user is not None:
            auth.login(request,user)
            return redirect('index')
        else:
            messages.info(request,"Invalid Username or Password")
            return redirect('login')
    else:
        return render(request,'login.html')
    
@login_required
def index(request):
    return render(request,'index.html')

@login_required
def addTasks(request):
    if request.method == 'POST':
        getTitle = request.POST['title']
        getDiscription = request.POST['discription']
        getDate = request.POST['date']
        task.objects.create(user=request.user,title = getTitle, discription = getDiscription , lastDate = getDate)

    return render(request,'addTasks.html')

@login_required
def yourTasks(request):
    tasks = task.objects.filter(user = request.user)[::-1][:3] 
    taskCount =task.objects.filter(user = request.user)[::-1]
    return render(request,'yourTasks.html',{'tasks':tasks, 'taskCount' : taskCount})

def logout(request):
    auth.logout(request)
    return redirect('login')

def allTasks(request):
    tasks = task.objects.filter(user = request.user)[::-1]
    return render(request,'allTasks.html',{'tasks':tasks})

def delete(request,delId):
    delTask = get_object_or_404(task,id = delId,user = request.user )
    delTask.delete()
    return redirect('yourTasks')

def fullTask(request,fullId):
    full = task.objects.get(id = fullId)
    return render(request,'fullTask.html',{'tasks' : full})