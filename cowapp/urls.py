from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from cowapp import views

app_name = 'cowapp'
urlpatterns = [
    path('users/', views.UserList.as_view()),
    path('users/new/', views.UserCreate.as_view()),
    path('users/<int:pk>/', views.UserDetail.as_view()),

    path('cows/', views.CowList.as_view()),
    path('cows/<int:pk>/', views.CowDetail.as_view()),

    path('records/', views.RecordList.as_view()),
    path('records/<int:pk>/', views.RecordDetail.as_view()),
    path('records/cow/<int:cow>/', views.RecordList.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
