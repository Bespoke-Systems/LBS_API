from django.urls import path
from .views import authViews, userRegistration

urlpatterns = [
    path('login/', authViews.LoginJwtToken.as_view(), name="login"),
    path('register/', userRegistration.UserRegister.as_view(), name='register'),
    path('logout/', authViews.LogOutJwtToken.as_view(), name="logout"),
]
# urlpatterns += router.urls
