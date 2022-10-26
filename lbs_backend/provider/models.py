from django.db import models
from django.contrib.auth import get_user_model
from users.models import Gender, CustomUser
from locations.models import CenterLocation, CountyModel

User = get_user_model()


class ProviderModel(models.Model):
    UserID = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="UserProviderID")
    CountyID = models.ForeignKey(CountyModel, on_delete=models.CASCADE, related_name="provider_county", null=True)
    TimeStamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Service Providers"
        verbose_name_plural = "Service Providers"
        ordering = ['TimeStamp']

    def __str__(self):
        return str(self.UserID)


class ProviderService(models.Model):
    from services.models import Service, WorkingDays
    AGE = [
        ('18+', '18+'), ('All', 'All'),
        ('10+', '10+'), ('16+', '16+'),
    ]
    ProviderID = models.ForeignKey(ProviderModel, on_delete=models.CASCADE, related_name="providerID")
    ServiceTitle = models.CharField(max_length=250)
    ProductID = models.ForeignKey(Service, on_delete=models.PROTECT, related_name="providerProductID")
    CenterLocationID = models.ForeignKey(CenterLocation, on_delete=models.PROTECT, null=True, blank=True,
                                         related_name="providerLocation")
    ServiceDescription = models.TextField(null=True, blank=True)
    GenderID = models.ForeignKey(Gender, on_delete=models.PROTECT, null=True, blank=True,
                                 related_name="providerGenders")
    AgeBracket = models.CharField(max_length=9, choices=AGE, null=True, blank=True)
    workingDays = models.ManyToManyField(WorkingDays, related_name="workingdays")
    Longitude = models.CharField(max_length=50, blank=True, null=True)
    Lattitude = models.CharField(max_length=50, blank=True, null=True)
    TimeStamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Provider Services"
        verbose_name_plural = "Provider Services"
        ordering = ['-TimeStamp']

    def __str__(self):
        return "{} | {}".format(str(self.ProviderID), self.ServiceTitle)


class ServiceRequest(models.Model):
    UserID = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_requesting')
    ProviderServiceID = models.ForeignKey(ProviderService, on_delete=models.CASCADE)
    CenterLocationID = models.ForeignKey(CenterLocation, on_delete=models.DO_NOTHING, blank=True, null=True)
    Latitude = models.CharField(max_length=50, blank=True, null=True)
    Longitude = models.CharField(max_length=50, blank=True, null=True)
    TimeStamp = models.DateTimeField(auto_now_add=True)
    RequestText = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = "Services Requests"
        verbose_name_plural = "Services Requests"
        ordering = ['-TimeStamp']

    def __str__(self):
        return self.UserID.FirstName + " | " + self.ProviderServiceID.ServiceTitle


class ServiceResponse(models.Model):
    ServiceRequestID = models.ForeignKey(ServiceRequest, on_delete=models.CASCADE)
    ResponseText = models.TextField(null=True, blank=True)
    TimeStamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Services Responses"
        verbose_name_plural = "Services Responses"
        ordering = ['-TimeStamp']

    def __str__(self):
        return str(self.ServiceRequestID)
