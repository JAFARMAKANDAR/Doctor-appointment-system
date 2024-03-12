
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from management.views import *
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name="ManagementHome"),
    path('service/', Service, name="ManagementService"),
    path('about/', About, name="ManagementAbout"),
    path('register/', Register, name="ManagementRegister"),
    path('login/', Login, name="ManagementLogin"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
