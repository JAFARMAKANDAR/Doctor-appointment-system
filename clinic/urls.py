
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
    path('contact/', Contact, name="ManagementContact"),
    path('register/', Register, name="ManagementRegister"),
    path('admin_login/', Login, name='login'),
    path('logout/', Logout_admin, name='logout'),
    path('view_doctor/', View_Doctor, name='view_doctor'),
    path('view_patient/', View_Patient, name='view_patient'),
    path('view_appointment/', View_Appointment, name='view_appointment'),
    path('add_doctor/', Add_Doctor, name='add_doctor'),
    path('add_patient/', Add_Patient, name='add_patient'),
    path('add_appointment/', Add_Appointment, name='add_appointment'),
    path('delete_patient/(?p<int:pid>)/', Delete_Patient, name='delete_patient'),
    path('delete_appointment/(?p<int:pid>)/', Delete_Appointment, name='delete_appointment'),
    path('delete_doctor/(?p<int:pid>)/', Delete_Doctor, name='delete_doctor'),
    path('specialty/<str:specialty>/', specialty_doctors, name='specialty_doctors'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
