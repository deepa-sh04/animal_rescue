# animal_rescue/core/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('add_animal/', views.add_animal, name='add_animal'),
    path('pet_list/', views.animal_list, name='pet_list'),
    path('pet/<int:pet_id>/', views.pet_detail, name='pet_detail'),
    path('lost_pet/', views.lost_pet, name='lost_pet'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
]