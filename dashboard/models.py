from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Service(models.Model):
    Type = models.CharField(max_length=255, blank=True, null=True)
    contact_phone = models.CharField(max_length=255, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    urlhash = models.CharField(max_length=6, blank=True, null=True)
    contact_email = models.CharField(max_length=255, blank=True, null=True)
    description  = models.CharField(max_length=255, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    cost = models.FloatField(default=0.0)
    availability = models.NullBooleanField(max_length=5, default=1, verbose_name="Availability status")
    #attachment = models.ImageField(upload_to='dashboard', default='team-1.jpg')
    
    def __unicode__(self):
        return self.urlhash

class Images(models.Model):
    urlhash = models.CharField(max_length=6, blank=True, null=True)
    attachment = models.FileField(upload_to='dashboard', blank=True, null=True)

    def __unicode__(self):
        return self.urlhash
    class Meta:
        verbose_name_plural = 'Images'


class Bookings(models.Model):
    urlhash = models.ForeignKey(Service, on_delete=models.CASCADE,verbose_name="Reference Code")
    user = models.ForeignKey(User, on_delete=models.CASCADE,default=1)
    name = models.CharField(max_length=255)
    contact_phone = models.CharField(max_length=255)
    contact_email = models.CharField(max_length=255)
    start_date = models.DateField()
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    status = models.NullBooleanField(max_length=5, default=0, verbose_name="Payment status")
    mpesa_receipt_code = models.CharField(max_length=255, blank=True, null=True)

    def __unicode__(self):
        return self.urlhash

    class Meta:
        verbose_name_plural = 'Bookings'



# class Reports(models.Model):
#     urlhash = models.ForeignKey(Service, on_delete=models.CASCADE, verbose_name="Unique Code")
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     reference = models.CharField(max_length=255, verbose_name="Item Changed Reference")
#     message = models.CharField(max_length=255)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __unicode__(self):
#         return self.urlhash

#     class Meta:
#         verbose_name_plural = 'User Actions Reports'


class Transaction(models.Model):
    mpesa_receipt_number = models.CharField(max_length=255, blank=True, null=True)
    amount = models.FloatField(max_length=30, default=0.0, verbose_name="Amount transacted")
    phone = models.CharField(max_length=15, blank=True, null=True)
    last_updated = models.DateTimeField(auto_now_add=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Initiated By")
    status = models.NullBooleanField(max_length=5, default=1)


class C2BMessage(models.Model):
    """
    Handles C2B Requests
    """
    transaction_id = models.CharField(max_length=20, unique=True)
    transaction_date = models.DateTimeField(blank=True, null=True)
    amount = models.FloatField(max_length=30, blank=True, null=True)
    business_short_code = models.CharField(
        max_length=20, blank=True, null=True)
    bill_ref_number = models.CharField(max_length=50, blank=True, null=True)
    invoice_number = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(blank=True, max_length=16, null=True)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return '{} {} {}'.format(self.first_name, self.middle_name, self.last_name)


class OnlineCheckoutResponse(models.Model):
    """
    Handles Online Checkout Response
    """
    id = models.BigAutoField(primary_key=True)
    merchant_request_id = models.CharField(max_length=50, blank=True, null=True)
    checkout_request_id = models.CharField(max_length=50, default='')
    result_code = models.CharField(max_length=5, blank=True, null=True)
    result_description = models.CharField(max_length=100, blank=True, null=True)
    mpesa_receipt_number = models.CharField(max_length=50, blank=True, null=True)
    transaction_date = models.DateTimeField(blank=True, null=True)
    phone = models.BigIntegerField(blank=True, null=True)
    amount = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return str(self.phone)

    class Meta:
        db_table = 'tbl_online_checkout_responses'
        verbose_name_plural = 'Online Checkout Responses'
