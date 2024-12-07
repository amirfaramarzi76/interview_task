from django.urls import path
from .views import upload_json

urlpatterns = [
    path('', upload_json, name='json'),
]