from __future__ import absolute_import ,unicode_literals
import django_tables2 as tables
from django.utils.html import format_html
from django_tables2.utils import A
from django.urls import reverse
from dashboard.models import Service, Images, Transaction, C2BMessage, OnlineCheckoutResponse, Bookings

class ServiceTable(tables.Table):
	#edit = tables.LinkColumn('process_payment',args=[A('pk')],verbose_name="Action",orderable=False,empty_values=())
	#editable =  CheckBoxColumnWithName(verbose_name="Select", accessor="pk")
	urlhash = tables.LinkColumn('service_expand',args=[A('pk')],verbose_name="Reference Code",orderable=True,empty_values=())
	def render_edit(self,record):
		if Bookings.objects.values_list('status', flat=True).get(order_number=record.pk) == False:
			return format_html('<a href='+reverse("accept", args=[record.pk])+'><button type="button" class="form-control btn-success">initiate payment(Kshs 200)</button></a>')
		else:
			return format_html('<a href="#"><p>Paid</p></a>')


	class Meta:
		model = Service
		fields = ('urlhash','Type','location','contact_phone','contact_email','availability')


class BookingsTable(tables.Table):
	edit = tables.LinkColumn('process_payment', args=[A(
	    'pk')], verbose_name="Action", orderable=False, empty_values=())

	def render_edit(self, record):
		if Bookings.objects.values_list('status', flat=True).get(id=record.pk) == False:
			return format_html('<a href='+reverse("process_payment", args=[record.pk])+'><button type="button" class="form-control btn-success">Pay via Mpesa</button></a>')
		else:
			return format_html('<a href="#"><p>Paid</p></a>')
	class Meta:
		model = Bookings
		fields = ('urlhash', 'user', 'name', 'contact_phone',
                  'contact_email', 'start_date', 'message','status')


class BookingsTable1(tables.Table):
	
	class Meta:
		model = Bookings
		fields = ('urlhash', 'user', 'name', 'contact_phone',
                    'contact_email', 'start_date', 'message', 'status')

class TransactionTable(tables.Table):
    class Meta:
        model = Transaction
        fields = ("mpesa_receipt_number", 'user_id',
                  'amount', "phone", 'status', 'last_updated')
