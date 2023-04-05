from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from drf_yasg.generators import OpenAPISchemaGenerator

class CustomOpenAPISchemaGenerator(OpenAPISchemaGenerator):
  def get_schema(self, request=None, public=False):
    """Generate a :class:`.Swagger` object with custom tags"""

    swagger = super().get_schema(request, public)
    swagger.tags = [
        {
            "name": "User",
            "description": "For using th API you need(mostly) to register as a user. Registering gives you all"
                           " the the non admin access endpoints. After Registration you need to get your JWT access token "
                           "to send requests to the API endpoints"
        },
    ]

    return swagger

admin.site.site_header = "Location Based Mobile Advertising System Database "
admin.site.index_title = "Applications"


schema_view = get_schema_view(
   openapi.Info(
      title="Nipate data source and API", default_version='v1.0', description="LBS APIs Doc",
      terms_of_service="https://www.google.com/policies/terms/", contact=openapi.Contact(email="amosditto@gmail.com"),
      license=openapi.License(name="BSD License"),
   ), public=True, permission_classes=[permissions.AllowAny], generator_class=CustomOpenAPISchemaGenerator,
)
urlpatterns = [
   # default project urls
   path('admin/', admin.site.urls),
   path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

   #  applications urls
   path('auth/', include('users.urls')),
   path('service/', include("services.urls")),
   path('location/', include('locations.urls')),
]

if bool(settings.DEBUG):
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)