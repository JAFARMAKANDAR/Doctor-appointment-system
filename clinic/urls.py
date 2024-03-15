
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from management.views import *
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name="home"),
    path('service/', Service, name="ManagementService"),
    path('about/', About, name="ManagementAbout"),
    path('register/', Register, name="ManagementRegister"),
    path('admin_login/', Login, name='login'),
    path('logout/', Logout_admin, name='logout'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
