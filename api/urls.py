from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

from . import views


app_name = 'api'

urlpatterns = [
    path('', views.SnapshotList.as_view()),
    path('api/v1/stations/', views.SnapshotList.as_view()),
    path('api/v1/stations/<int:kioskID>/', views.SnapshotDetail.as_view()),
]
