import pytest
from rest_framework.test import APIClient
from django.urls import reverse

client = APIClient()
login_url = reverse('login')
registration_url = reverse('user')


@pytest.mark.django_db
def test_login_user(user):
    response = client.post(login_url, dict(MobileNumber='0794818111', password='ilovemagic'))
    assert response.status_code == 200


@pytest.mark.django_db
def test_register_user(location, gender):
    personal_details = dict(
        MobileNumber='0794818112', IDNumber='38598119', password='where123', FirstName='Anthony',
        SurName='Fu'
    )
    app_details = dict(GenderID=gender.id, LocationID=location.id)
    response = client.post(registration_url, data=dict(**personal_details, **app_details))
    assert response.status_code == 201
