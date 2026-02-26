from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    MedicalRecordListCreateView,
    MedicalRecordDetailView,
    PatientListView,
    MedicationCreateView,
    MedicationDetailView,
    # ObservationListCreateView,
    ObservationDetailView,
    PatientProfileView,
    PatientMedicalRecordListView,
    PatientMessageCreateView,
    PatientMessageListView,
    RegisterView,
    DoctorMessageListView,
    DoctorReplyMessageView,
    PrescriptionCreateView

)

urlpatterns = [
    path('profile/', PatientProfileView.as_view(), name='profile_list'),

    #doctor model uchun
    path('medical-records/',MedicalRecordListCreateView.as_view(), name='medical_record_list'),
    path('medical-records/<int:pk>/',MedicalRecordDetailView.as_view(), name='medical_record_list'),

    #Nurse model uchun
    path('medications/',MedicationCreateView.as_view(), name='medication_list'),
    path('medications/<int:pk>/', MedicationDetailView.as_view(), name='medication_edit'),
    path('prescriptions/create/', PrescriptionCreateView.as_view(), name='prescription_create'),

    # path('observations/',ObservationListCreateView.as_view(), name='observation_list'),
    path('observations/<int:pk>', ObservationDetailView.as_view(), name='observation_list'),

    #patient uchun
    path('patients/list/',PatientListView.as_view(), name='patient_list'),
    path('patients/records/',PatientMedicalRecordListView.as_view(), name='medical_record_list'),
    path('patients/message/',PatientMessageCreateView.as_view(), name='message_create'),
    path('patients/message/', PatientMessageListView.as_view(), name='message_list'),
    path('doctor/message/', DoctorMessageListView.as_view(), name='message_list'),
    path('doctor/replay/', DoctorReplyMessageView.as_view(), name='message_list'),

    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]