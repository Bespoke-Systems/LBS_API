from django.db import models
from django.contrib.auth import get_user_model
from locations.models import (TownsModel)
from users.models import Gender

UserModel = get_user_model()

class ProductCategory(models.Model):
    Name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Product Categories"
        verbose_name_plural = "Product Categories"
    def __str__(self):
        return self.Name

class Product(models.Model):
    CategoryID = models.ForeignKey(ProductCategory, on_delete=models.PROTECT, related_name="category")
    Name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Products"
        verbose_name_plural = "Products"

class WorkingDays(models.Model):
    DAYS_OF_WEEK = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    ]
    days = models.CharField(max_length=9, choices=DAYS_OF_WEEK)

    class Meta:
        verbose_name = "Potential Working Days"
        verbose_name_plural = "Potential Working Days"
    
    def __str__(self):
        return self.days


# -----> Provider Details Model
class ServiceProvider(models.Model):

    AGE = [
        ('18+', '18+'),
        ('All', 'All'),
        ('10+', '10+'),
        ('16+', '16+'),
    ]
    UserID = models.OneToOneField(UserModel, on_delete=models.CASCADE, related_name="UserID")
    ProductID = models.ForeignKey(Product, on_delete=models.PROTECT, related_name="ProductID")
    LocationID = models.ForeignKey(TownsModel, on_delete=models.PROTECT, null=True, blank=True, related_name="LocationID")
    GenderID = models.ForeignKey(Gender, on_delete=models.PROTECT,null=True,blank=True, related_name="GenderID")
    AgeBracket = models.CharField(max_length=9, choices=AGE, null=True, blank=True)
    WorkingDays = models.ManyToManyField(WorkingDays, related_name="working_days")
    TimeStamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Service Providers"
        verbose_name_plural = "Service Providers"
    
    def __str__(self):
        return "%s || %s" % (str(self.id), str(self.UserID))


class ServiceRequest(models.Model):
    ProductID = models.ForeignKey(Product, on_delete=models.PROTECT, related_name="product")
    UserID = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name="user")
    LocationID = models.ForeignKey(TownsModel, on_delete=models.PROTECT, null=True, blank=True, related_name="location")
    Timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Requested Services"
        verbose_name_plural = "Requested Services"
    def __str__(self):
        return "%s || %s" % (str(self.ProductID), str(self.UserID))