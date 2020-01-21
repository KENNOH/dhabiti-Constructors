from django.shortcuts import render
from accounts.models import specialization
from accounts.models import Profile
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
)
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from accounts.models import specialization
from dashboard.models import Images, Service
# Create your views here.

def create_booking(request,urlhash):
    details = Profile.objects.get(pk=pk)
    u = User.objects.all().get(pk=details.user.pk)
    return render(request, 'home/read_more.html', {'details': details,'u':u})

def home(request):
    s = specialization.objects.all()
    services = Service.objects.all()
    images = Images.objects.all()
    return render(request,'home/index.html',{'s':s,'services':services,'images':images})

def view_service(request,urlhash):
    item = Service.objects.all().get(urlhash=urlhash)
    return render(request,'home/expand.html',{'item':item})

def filter_services(request,Username):
    spec = specialization.objects.all().get(name__icontains=Username).name
    services = Service.objects.all().filter(Type=spec)
    s = specialization.objects.all()
    images = Images.objects.all()
    return render(request,'home/index.html',{'s':s,'services':services,'images':images})
