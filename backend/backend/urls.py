from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from django.http import HttpResponse
from environment.views import EnvironmentDataViewSet, UploadCSV

router = routers.DefaultRouter()
router.register(r'environment', EnvironmentDataViewSet)

def index(request):
    return HttpResponse("Smart Kigali API is running. Visit /api/environment/ for data endpoints.")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('environment/upload/', UploadCSV.as_view(), name='environment-upload'),
    path('', index, name='index'),
]
