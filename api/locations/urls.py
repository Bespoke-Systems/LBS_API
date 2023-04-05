from django.urls import path
from . import views

urlpatterns = [
    path("counties/", views.CountyView.as_view(), name="counties"),
    path("towns/", views.TownsView.as_view(), name="towns"),
    path("locations/", views.LocationApi.as_view(), name="locations"),
]