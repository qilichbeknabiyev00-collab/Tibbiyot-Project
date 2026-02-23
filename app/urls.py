from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MedicalRecordViewSet, ObservationViewSet, PatentProfileViewSet, treatment_suggestion
from .views import StatisticsView
router = DefaultRouter()
router.register(r'medical-records', MedicalRecordViewSet)
router.register(r'observations', ObservationViewSet)
router.register(r'patients', PatentProfileViewSet, basename='patients')

urlpatterns = [
    path('', include(router.urls)),
    path('treatment-suggestion/', treatment_suggestion, name='treatment_suggestion'),
    path('statistics/', StatisticsView.as_view(), name='statistics'),
]