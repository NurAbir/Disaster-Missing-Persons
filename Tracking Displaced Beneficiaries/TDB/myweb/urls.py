from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add/', views.add_missing_person, name='add_missing_person'),
    path('person/<int:pk>/', views.person_detail, name='person_detail'),
]