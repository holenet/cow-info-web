from django.urls import path

from cowapp import views

app_name = 'cowapp'
urlpatterns = [
    path('', views.test, name='test'),
]
