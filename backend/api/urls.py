from django.urls import path
from .views import simple_api

urlpatterns = [
    path('simpleapi/', simple_api, name='simple_api'),
]