from django.urls import path
from . import views

urlpatterns=[
    path('',views.demo1),
    path('search',views.demo2)
]