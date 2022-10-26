import datetime

from django.db import models
from django.contrib.auth import get_user_model
from users.models import Gender
from locations.models import CountyModel

UserModel = get_user_model()


class ServiceCategory(models.Model):
    Name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Service Categories"
        verbose_name_plural = "Service Categories"

    def __str__(self):
        return self.Name


class Service(models.Model):
    CategoryID = models.ForeignKey(ServiceCategory, on_delete=models.PROTECT, related_name="category")
    Name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Services"
        verbose_name_plural = "Services"

    def __str__(self):
        return self.Name


class WorkingDays(models.Model):
    DAYS_OF_WEEK = [
        ('Monday', 'Monday'), ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'), ('Thursday', 'Thursday'),
        ('Friday', 'Friday'), ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    ]
    days = models.CharField(max_length=9, choices=DAYS_OF_WEEK)

    class Meta:
        verbose_name = "Potential Working Days"
        verbose_name_plural = "Potential Working Days"

    def __str__(self):
        return self.days


class Advertisement(models.Model):
    from provider.models import ProviderModel
    ADTitle = models.CharField(max_length=200, null=True, blank=True)
    ProviderID = models.ForeignKey(ProviderModel, null=True, on_delete=models.CASCADE)
    ServiceID = models.ManyToManyField(Service)
    LocationID = models.ForeignKey(CountyModel, on_delete=models.CASCADE)
    GenderID = models.ForeignKey(Gender, on_delete=models.PROTECT, null=True, blank=True)
    AdDescription = models.TextField(null=True, blank=True)
    StartDate = models.DateField(default=datetime.date.today)
    ExpiryDate = models.DateField()
    NoOfMessages = models.IntegerField(null=True, blank=True)

    REQUIRED_FIELDS = ['ProviderID']

    class Meta:
        verbose_name = "Advertisements"
        verbose_name_plural = "Advertisements"

    def __str__(self):
        return str(self.ADTitle + " | " + str(self.ExpiryDate))
