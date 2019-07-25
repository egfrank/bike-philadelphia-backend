from django.contrib import admin
from django.urls import include, path

from . import views


app_name = 'api'

urlpatterns = [
    # path('', views.index, name='index'),
    path('', views.SnapshotList.as_view()),
    path('api/v1/stations/', views.SnapshotList.as_view()),
    path('api/v1/stations/<int:kioskID>/', views.SnapshotDetail.as_view()),
]

