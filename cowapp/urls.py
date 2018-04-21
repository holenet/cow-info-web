from django.urls import path

from cowapp import views

app_name = 'cowapp'
urlpatterns = [
    path('cows/', views.CowList.as_view()),
    path('cows/<int:pk>/', views.CowDetail.as_view()),
    path('records/', views.RecordList.as_view()),
    path('records/<int:pk>/', views.RecordDetail.as_view()),
    path('records/cow/<int:pk>/', views.RecordList.as_view()),
]
