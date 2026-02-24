from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MedicalRecordListCreateView, MedicalRecordDetailView

urlpatterns = [

    path('medical-records/',MedicalRecordListCreateView.as_view(), name='medical_record_list'),
    path('medical-records/<int:pk>/',MedicalRecordDetailView.as_view(), name='medical_record_list'),





]