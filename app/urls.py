from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MedicalRecordViewSet, ObservationViewSet, PatentProfileViewSet

router = DefaultRouter()
router.register(r'medical-records', MedicalRecordViewSet)
router.register(r'observations', ObservationViewSet)
router.register(r'patients', PatentProfileViewSet, basename='patients')

urlpatterns = [
    path('', include(router.urls)),
]