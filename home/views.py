from django.http import HttpResponse
from rest_framework.decorators import api_view
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
from .access_token import lipa_na_mpesa
from django.views.decorators.csrf import csrf_exempt
import base64
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.mail import EmailMultiAlternatives
from rest_framework.response import Response
import logging
from decimal import Decimal
logger = logging.getLogger(__name__)
from dashboard.models import Transaction

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


def process_payment(request,id):
    b = Bookings.objects.get(id=id)
    phone = b.contact_phone
    amount = 1
    try:
        data = {"phone":phone,"amount":amount,'id':id}
        lipa_na_mpesa(data)
        messages.info(request, "Payment Initiated.Check your phone and enter pin to confirm.")
        return HttpResponseRedirect('/view_client_bookings/')
    except:
        messages.info(request, "There was an issue processing the payment ,Please try again.")
        return HttpResponseRedirect('/view_client_bookings/')


@csrf_exempt
def process_lnm(request):
    con = json.loads(request.read().decode('utf-8'))
    con1 = con["Body"]
    data = con1["stkCallback"]
    update_data = dict()
    update_data['result_code'] = data['ResultCode']
    update_data['result_description'] = data['ResultDesc']
    update_data['checkout_request_id'] = data['CheckoutRequestID']
    update_data['merchant_request_id'] = data['MerchantRequestID']
    meta_data = data['CallbackMetadata']['Item']
    if len(meta_data) > 0:
        # handle the meta data
        for item in meta_data:
            if len(item.values()) > 1:
                key, value = item.values()
                if key == 'MpesaReceiptNumber':
                    update_data['mpesa_receipt_number'] = value
                if key == 'Amount':
                    update_data['amount'] = Decimal(value)
                    a = update_data['amount']
                if key == 'PhoneNumber':
                    update_data['phone'] = int(value)
                    p = update_data['phone']
                if key == 'TransactionDate':
                    date = str(value)
                    year, month, day, hour, min, sec = date[:4], date[4:-
                                                    8], date[6:-6], date[8:-4], date[10:-2], date[12:]
                    update_data['transaction_date'] = '{}-{}-{} {}:{}:{}'.format(
                        year, month, day, hour, min, sec)
    v = Bookings.objects.get(mpesa_receipt_code=data['CheckoutRequestID'])
    v.status = 1
    v.save()
    Transaction.objects.create(user_id=v.user, amount=update_data['amount'], phone=update_data['phone'], mpesa_receipt_number=update_data['mpesa_receipt_number'])
    message = {"ResultCode": 0, "ResultDesc": "The service was accepted successfully",
               "ThirdPartyTransID": "freelance"}
    return JsonResponse({'message': message})
