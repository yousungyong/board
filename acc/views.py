from django.shortcuts import redirect, render
from .models import User
from django.contrib.auth import authenticate, login, logout
# Create your views here.

def index(request):
    return render(request, "base.html")

def login_user(request):
    if request.user.username:
        return redirect("acc:index")
    if request.method == "POST":
        u = request.POST.get("username")
        p = request.POST.get("password")
        user = authenticate(username=u, password=p)
        if user:
            login(request, user)
            return redirect("acc:index")        
    return render(request, "acc/login.html")

def logout_user(request):
    logout(request)
    return redirect("acc:index")

def signup(request):
    if request.user.username:
        return redirect("acc:index")
    if request.method == "POST":
        u = request.POST.get("username")
        p = request.POST.get("password")
        n = request.POST.get("nickname")
        a = request.POST.get("age")
        c = request.POST.get("comment")
        i = request.FILES.get("image")
        if not i:
            i = 'none.png'
        User.objects.create_user(username=u, password=p, nickname=n, age=a, comment=c, pic=i).save()
        return redirect("acc:login")
    return render(request, "acc/signup.html")

def profile(request):
    return render(request, "acc/profile.html")

def update(request):
    if request.method == "POST":
        u = request.user.username
        user = User.objects.get(username=u)
        p = request.POST.get("password")
        user.set_password(p)
        user.nickname = request.POST.get("nickname")
        user.age = request.POST.get("age")
        user.comment = request.POST.get("comment")
        i = request.FILES.get("image")
        if i:
            user.pic=i
        user.save()
        user= authenticate(username=u, password=p)
        login(request, user)
        return redirect("acc:profile")
    return render(request, "acc/update.html")

def delete(request):
    u = request.user.username
    user = User.objects.get(username=u)
    user.delete()
    return redirect("acc:index")