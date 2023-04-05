from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, MobileNumber, IDNumber, FirstName, password=None):
        if not MobileNumber:
            raise ValueError('you must enter your MobileNumber')
        if not IDNumber:
            raise ValueError('you must enter your IDNumber')
        if not FirstName:
            raise ValueError('you must enter your FirstName')

        user = self.model(
            MobileNumber=MobileNumber,
            IDNumber=IDNumber,
            FirstName=FirstName,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, MobileNumber, IDNumber, FirstName, password=None):
        user = self.create_user(MobileNumber, IDNumber, FirstName, password)
        user.is_admin = True
        user.save(using=self._db)
        return user
