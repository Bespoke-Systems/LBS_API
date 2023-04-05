from ..models import ServiceRequest, ServiceProvider


def get_service_providers(data):
    if "ProviderID" in data:
        providers = ServiceProvider.objects.filter(id=data["ProviderID"])
        return providers

    elif "ProductID" in data and "LocationID" in data:
        providers = ServiceProvider.objects.filter(ProductID_id=data["ProductID"], LocationID_id=data["LocationID"])
        return providers

    elif "ProductID" in data:
        providers = ServiceProvider.objects.filter(ProductID_id=data["ProductID"])
        return providers

    elif "LocationID" in data:
        providers = ServiceProvider.objects.filter(LocationID_id=data["LocationID"])
        return providers
    else:
        providers = ServiceProvider.objects.all()
        return providers


def get_services_requests(data):
    if "ProductID" in data and "UserID" in data and "LocationID" in data:
        requests = ServiceRequest.objects.filter(ProductID_id=data["ProductID"], UserID_id=data["UserID"],
                                                 LocationID_id=data["LocationID"])
        return requests
    elif "ProductID" in data and "UserID" in data:
        requests = ServiceRequest.objects.filter(UserID_id=data["UserID"], ProductID_id=data["ProductID"])
        return requests

    elif "LocationID" in data and "UserID" in data:
        requests = ServiceRequest.objects.filter(UserID_id=data["UserID"], LocationID_id=data["LocationID"])
        return requests

    elif "UserID" in data:
        requests = ServiceRequest.objects.filter(UserID_id=data["UserID"])
        return requests

    elif "LocationID" in data:
        requests = ServiceRequest.objects.filter(LocationID_id=data["LocationID"])
        return requests

    elif "ProductID" in data:
        requests = ServiceRequest.objects.filter(ProductID_id=data["ProductID"])
        return requests

    else:
        requests = ServiceRequest.objects.all()
        return requests
