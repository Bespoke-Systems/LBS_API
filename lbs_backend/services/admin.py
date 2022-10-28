from django.contrib import admin
from .models import (
    WorkingDays, ServiceCategory, Service, Advertisement
)

admin.site.register(ServiceCategory)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['id', 'Name']


@admin.register(WorkingDays)
class WorkingDaysAdmin(admin.ModelAdmin):
    list_display = ["id", "days"]


@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    list_display = [
        "id", "ADTitle", "UserID", "LocationID", "AdDescription", "StartDate", "ExpiryDate",
        "NoOfMessages"
    ]
