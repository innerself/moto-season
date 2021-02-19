from django.urls import path

from temperature import views

app_name = 'temperature'

urlpatterns = [
    path('', views.main, name='main'),
]
