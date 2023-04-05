import pytest

from users.models import CustomUser, Gender
from locations.models import CountyModel, TownsModel


@pytest.fixture()
def gender():
    gender = dict(name='Male')
    gender = Gender.objects.create(**gender)
    return gender


@pytest.fixture()
def user():
    user_data_a = dict(
        MobileNumber='0794818111', IDNumber='38598118', FirstName='Bob',
        password='ilovemagic'
    )
    user = CustomUser.objects.create_user(**user_data_a)
    return user


@pytest.fixture()
def location():
    county = CountyModel.objects.create(Name='Nakuru')
    town = TownsModel.objects.create(Name='Kabarak', County_id=county.id)
    return town
