from django.contrib import admin
from dashboard.models import  Service, Bookings

# Register your models here.


class EventModelAdmin(admin.ModelAdmin):
    list_display = ["urlhash", "Type", "contact_phone", "contact_email","location", "cost", "availability", "created_at"]
    list_display_links = ["urlhash"]
    list_filter = []
    list_per_page = 20
    list_editable = []

    class Meta:
        model = Service


class EventModelAdmin1(admin.ModelAdmin):
    list_display = ["id","urlhash", "user", "name","contact_phone",
                    "contact_email", "status", "mpesa_receipt_code", "created_at","message"]
    list_display_links = ["id"]
    list_filter = []
    list_per_page = 20
    list_editable = []

    class Meta:
        model = Bookings


admin.site.register(Service, EventModelAdmin)
admin.site.register(Bookings, EventModelAdmin1)
