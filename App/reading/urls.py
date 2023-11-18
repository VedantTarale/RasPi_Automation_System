from django.urls import path
from .views import *
urlpatterns = [
    path('',index),
    path('add_reading/',add_reading)
]
