
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="ManagementHome"),
    path('base', views.BASE, name='base'),

]
