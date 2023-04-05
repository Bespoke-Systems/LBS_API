from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .managers import UserManager
from locations.models import TownsModel


# ----> Gender Table

class Gender(models.Model):
    name = models.CharField(max_length=6)

    class Meta:
        verbose_name = 'Gender'
        verbose_name_plural = 'Gender'

    def __str__(self):
        return str(self.name)


# ----> User Table

class CustomUser(AbstractBaseUser):
    MobileNumber = models.CharField(max_length=12, unique=True)
    IDNumber = models.CharField(max_length=15, null=True, blank=True)
    GenderID = models.ForeignKey(Gender, on_delete=models.CASCADE, null=True, blank=True)
    YearOfBirth = models.DateField(null=True, blank=True)
    FirstName = models.CharField(max_length=50, null=True, blank=True)
    MiddleName = models.CharField(max_length=50, null=True, blank=True)
    SurName = models.CharField(max_length=50, null=True, blank=True)
    LocationID = models.ForeignKey(TownsModel, on_delete=models.PROTECT, null=True, blank=True)
    ADBalance = models.FloatField(default=0, null=True, blank=True)
    DateCreated = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'MobileNumber'
    REQUIRED_FIELDS = ['IDNumber', 'FirstName']

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.MobileNumber

    @staticmethod
    def has_perm(perm, obj=None):
        return True

    @staticmethod
    def has_module_perms(app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
