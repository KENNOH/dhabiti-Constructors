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
from dashboard.models import Images, Service, Bookings
from dashboard.forms import BookForm
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from dashboard.tables import BookingsTable
from django_tables2 import RequestConfig
# Create your views here.


@login_required(login_url='/accounts/login/')
def create_booking(request,urlhash):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            name = request.user.first_name + " " + request.user.last_name
            contact_email = request.user.email
            request.user.refresh_from_db()
            contact_phone = request.user.profile.phone
            start_date = form.cleaned_data['start_date']
            message = form.cleaned_data['message']
            code = Service.objects.get(urlhash=urlhash)
            Bookings.objects.create(contact_email=contact_email,urlhash=code,user=request.user,name=name,contact_phone=contact_phone,start_date=start_date,message=message)
            messages.info(request, "Booked successfully.")
            return HttpResponseRedirect('/view_client_bookings/')
        else:
            return render(request, 'home/read_more.html', {"form": form})
    else:
        form = BookForm()
        args = {'form':form}
        return render(request, 'home/read_more.html',args)


def variables():
    s = specialization.objects.all()
    services = Service.objects.all()
    images = Images.objects.all()
    dataset = {'s':s,'services':services,'images':images}
    return dataset


@login_required(login_url='/accounts/login/')
def view_client_bookings(request):
    trans = BookingsTable(Bookings.objects.all().filter(user_id=request.user))
    RequestConfig(request, paginate={"per_page": 20}).configure(trans)
    return render(request, 'home/my_bookings.html', {'bookings': trans})

def home(request):
    return render(request, 'home/index.html', {'s': variables().get('s'), 'services': variables().get('services'), 'images': variables().get('images')})

def view_service(request,urlhash):
    item = Service.objects.all().get(urlhash=urlhash)
    images = Images.objects.all().filter(urlhash=urlhash)
    return render(request,'home/expand.html',{'item':item,'images':images})

def filter_services(request,Username):
    spec = specialization.objects.all().get(name__icontains=Username).name
    services = Service.objects.all().filter(Type=spec)
    s = specialization.objects.all()
    images = Images.objects.all()
    return render(request,'home/index.html',{'s':s,'services':services,'images':images})
