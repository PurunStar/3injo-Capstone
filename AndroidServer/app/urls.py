from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('initxy/<xy>', views.initxy),
    path('addstack/<xy>/<stack>', views.addstack),
    path('substack/<xy>', views.substack),
    path('getFlag', views.getFlag),
    path('sendLine/<ln>/' , views.setLine),
]
