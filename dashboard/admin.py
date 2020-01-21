from django.contrib import admin
from dashboard.models import  Service

# Register your models here.


class EventModelAdmin(admin.ModelAdmin):
    list_display = ["Type","contact_phone","contact_email","urlhash","location","status","cost","availability","created_at"]
    list_display_links = ["name"]
    list_filter = []
    list_per_page = 20
    list_editable = []

    class Meta:
        model = Service