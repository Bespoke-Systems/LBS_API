from django.contrib import admin
from .models import (
    WorkingDays, ProductCategory, Product, ServiceProvider, ServiceRequest, RequestResponse, Advertisement
)

class WorkingDaysAdmin(admin.ModelAdmin):
    list_display = ["id", "days"]

class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'Name']

class ServiceProviderAdmin(admin.ModelAdmin):
    list_display = ['id', 'UserID', 'ProductID', 'LocationID', 'GenderID', 'TimeStamp']

class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = ['id', 'UserID', 'ProductID', 'LocationID', 'Timestamp']

class ServiceRequestResponseAdmin(admin.ModelAdmin):
    list_display = ['id', 'RequestID', 'ProviderID', 'Timestamp']

class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ['id', 'UserID', 'ProductID', 'LocationID', 'GenderID', 'Timestamp', 'ExpiryDate']

admin.site.register(WorkingDays, WorkingDaysAdmin)
admin.site.register(ProductCategory)
admin.site.register(Product, ProductAdmin)
admin.site.register(ServiceProvider, ServiceProviderAdmin)
admin.site.register(ServiceRequest, ServiceRequestAdmin)
admin.site.register(RequestResponse, ServiceRequestResponseAdmin)
admin.site.register(Advertisement, AdvertisementAdmin)