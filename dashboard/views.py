from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import user_passes_test
import os
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import UserChangeForm
import time
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
)
from django.contrib.auth.models import Group
from .forms import UpdateProfile,ServiceForm
from accounts.models import Profile
from django.http import HttpResponseRedirect
from accounts.models import specialization
from .models import Images,Service,Transaction, C2BMessage, OnlineCheckoutResponse,Bookings
import string ,random
from .tables import ServiceTable, TransactionTable, BookingsTable, BookingsTable1
from django_tables2 import RequestConfig
from .render import Render
from django.template.loader import get_template
from xhtml2pdf import pisa
from .utils import render_to_pdf
from django.http import HttpResponse
import datetime


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
		return ''.join(random.choice(chars) for _ in range(size))


def id_generator2(size=5, chars=string.ascii_uppercase):
		return ''.join(random.choice(chars) for _ in range(size))

@login_required(login_url='/accounts/login/')
@user_passes_test(lambda u: u.groups.filter(name='Service Provider').exists())
def client_home(request):
	s = specialization.objects.all()
	services = Service.objects.all()
	images = Images.objects.all()
	return render(request, 'home/index.html',{'s':s,'services':services,'images':images})


@login_required(login_url='/accounts/login/')
@user_passes_test(lambda u: u.groups.filter(name='Service Provider').exists())
def service_provider_home(request):
	services = ServiceTable(Service.objects.all().filter(user=request.user).order_by('-created_at'))
	RequestConfig(request, paginate={"per_page": 20}).configure(services)
	return render(request, 'dashboard/service_provider.html', {'services': services})


@login_required(login_url='/accounts/login/')
@user_passes_test(lambda u: u.groups.filter(name='Service Provider').exists())
def update_worker(request):
	p = Profile.objects.get(user_id=request.user)
	if request.method == "POST":
		form = UpdateProfile(request.POST, request.FILES, instance=request.user)
		if form.is_valid():
			if bool(form.cleaned_data.get('display_pic', False)) == False:
				form.save()
				messages.info(request, 'Profile updated successfully.')
				return HttpResponseRedirect('/dashboard/worker/')
			else:
				m = form.cleaned_data['display_pic']
				obj = p
				# if bool(obj.display_pic) == True:
				# 	if not str(obj.display_pic.name) == 'accounts/empty-profile.jpg':
				# 		os.remove(obj.display_pic.path)
				obj.display_pic = m
				form.save()
				obj.save()
				messages.info(request, 'Profile updated successfully.')
				return HttpResponseRedirect('/dashboard/worker/')
		else:
			form = UpdateProfile(instance=request.user)
			args = {'form': form, 'p': p}
			messages.info(request, 'Sorry ,there are errors in your form, fix them to continue.')
			return render(request, 'dashboard/worker_profile.html', args)
	else:
		form = UpdateProfile(instance=request.user)
		args = {'form': form, 'p': p}
		return render(request, 'dashboard/worker_profile.html', args)


@login_required(login_url='/accounts/login/')
@user_passes_test(lambda u: u.groups.filter(name='Service Provider').exists())
def add(request):
	if request.method == 'POST':
		form = ServiceForm(request.POST, request.FILES)
		if form.is_valid():
			if not Service.objects.filter(user=request.user).count() >2:
				Type = form.cleaned_data['Type']
				email = request.user.email
				request.user.refresh_from_db()
				phone = request.user.profile.phone
				description = form.cleaned_data['description']
				loc = form.cleaned_data['location']
				cost = form.cleaned_data['cost']
				rand = id_generator()
				Service.objects.create(Type=Type,contact_email=email,cost=cost,contact_phone=phone,description=description,urlhash=rand,user=request.user,location=loc)
				for file in request.FILES.getlist("attachment2"):
					Images.objects.create(urlhash=rand,attachment=file)
				messages.info(request, "Processed successfully.")
				return HttpResponseRedirect('/dashboard/worker/')
			else:
				messages.info(request, "Sorry, you can only add a maximum of two service profiles.")
				return HttpResponseRedirect('/dashboard/worker/')
		else:
		    return render(request, 'dashboard/add.html', {"form": form})
	else:
	    form = ServiceForm()
	    args = {'form':form}
	    return render(request, 'dashboard/add.html',args)


@login_required(login_url='/accounts/login/')
@user_passes_test(lambda u: u.groups.filter(name='Service Provider').exists())
def trans(request):
    trans = TransactionTable(Transaction.objects.all().filter(user_id=request.user).order_by('-last_updated'))
    RequestConfig(request, paginate={"per_page": 20}).configure(trans)
    return render(request, 'dashboard/transaction.html', {'trans': trans})


@login_required(login_url='/accounts/login/')
@user_passes_test(lambda u: u.groups.filter(name='Service Provider').exists())
def service_expand(request,pk):
	service = Service.objects.all().get(id=pk)
	return render(request, 'dashboard/service_expand.html', {'form': service})


@login_required(login_url='/accounts/login/')
@user_passes_test(lambda u: u.groups.filter(name='Service Provider').exists())
def bookings(request):
	data = []
	for i in Service.objects.all().filter(user=request.user):
		data.append(i)
	trans = BookingsTable1(Bookings.objects.all().filter(urlhash__in=data))
	RequestConfig(request, paginate={"per_page": 20}).configure(trans)
	return render(request, 'dashboard/bookings.html', {'bookings': trans})


@login_required(login_url='/accounts/login/')
@user_passes_test(lambda u: u.groups.filter(name='Service Provider').exists())
def generate_report(request):
	hidden = request.POST['hidden']
	now = datetime.datetime.now()
	d = id_generator2()
	n = str(request.user.first_name).split()[0][0] + "." + str(request.user.last_name).split()[0][0]
	if hidden == 'transactions':
		data = []
		for i in Service.objects.all().filter(user=request.user):
			data.append(i)
		bookings = Bookings.objects.all().filter(urlhash__in=data)
		data2 = []
		for i in bookings:
			data2.append(i.contact_phone)
		trans = Transaction.objects.filter(phone__in=data2)
		template = get_template('dashboard/transactions_pdf.html')
		context = {'transactions': trans, 'now': now, 'd': d, 'n': n}
		html = template.render(context)
		pdf = render_to_pdf('dashboard/transactions_pdf.html', context)
		if pdf:
			response = HttpResponse(pdf, content_type='application/pdf')
			filename = "Transactions.pdf"
			content = "inline; filename='%s'" % (filename)
			download = request.GET.get("download")
			if download:
				content = "attachment; filename='%s'" % (filename)
			response['Content-Disposition'] = content
			return response
		else:
			return HttpResponse("Not found")


	if hidden == 'bookings':
		data = []
		for i in Service.objects.all().filter(user=request.user):
			data.append(i)
		bookings = Bookings.objects.all().filter(urlhash__in=data)
		template = get_template('dashboard/bookings_pdf.html')
		context = {'bookings': bookings, 'now': now, 'd': d, 'n': n}
		html = template.render(context)
		pdf = render_to_pdf('dashboard/bookings_pdf.html', context)
		if pdf:
			response = HttpResponse(pdf, content_type='application/pdf')
			filename = "Bookings.pdf"
			content = "inline; filename='%s'" % (filename)
			download = request.GET.get("download")
			if download:
				content = "attachment; filename='%s'" % (filename)
			response['Content-Disposition'] = content
			return response
		else:
			return HttpResponse("Not found")
