from django.http import HttpResponse
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
import requests
from .import keys
from datetime import datetime
import base64
import json
from django.http import JsonResponse
from django.core.mail import EmailMultiAlternatives
import logging
from requests.auth import HTTPBasicAuth
from decimal import Decimal
logger = logging.getLogger(__name__)
from dashboard.models import Bookings

def gen_access_token():
	import requests
	consumer_key = keys.key
	consumer_secret = keys.secret
	api_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
	r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))
	json_reponse = (r.json())
	my_access_token = json_reponse["access_token"]
	#print(my_access_token)
	return my_access_token


def lipa_na_mpesa(data):
	cost = data.get('amount')
	phone_number = data.get('phone')
	b = Bookings.objects.get(id=data.get('id'))
	timestamp = str(datetime.now())[:-7].replace('-','').replace(' ', '').replace(':', '')
	password = base64.b64encode(bytes('{}{}{}'.format(keys.paybill, keys.passkey, timestamp), 'utf-8')).decode('utf-8')
	api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
	headers = {"Authorization": "Bearer %s" % gen_access_token()}
	request = {
            "BusinessShortCode": keys.paybill,
            "Password": password,
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": cost,
            "PartyA": phone_number,
            "PartyB": keys.paybill,
            "PhoneNumber": phone_number,
            "CallBackURL": "https://87bcc595.ngrok.io/process_lnms/",
            "AccountReference": "dhabiti construction",
            "TransactionDesc": "dhabiti construction",
        }
	response = requests.post(api_url, json=request, headers=headers)
	print(response.text)
	h = json.loads(response.text)
	i = h['CheckoutRequestID']
	b.mpesa_receipt_code = i
	b.save()
