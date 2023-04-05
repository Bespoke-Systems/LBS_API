from django.contrib import admin
from .models import CountyModel, TownsModel


admin.site.register(CountyModel)
admin.site.register(TownsModel)