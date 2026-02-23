from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import MedicalRecord, Observation
from .serializers import MedicalRecordSerializer, ObservationSerializer,PatientProfileSerializer
from .permissions import IsDoctor, IsNurse, IsPatient
# Create your views here.

class MedicalRecordViewSet(viewsets.ModelViewSet):
    queryset = MedicalRecord.objects.all()
    serializer_class = MedicalRecordSerializer
    permission_classes = [IsAuthenticated,IsDoctor]

    def perform_create(self, serializer):
        serializer.save(doctor=self.request.user)

class ObservationViewSet(viewsets.ModelViewSet):
    queryset = Observation.objects.all()
    serializer_class = ObservationSerializer
    permission_classes = [IsAuthenticated,IsNurse]

    def perform_create(self, serializer):
        serializer.save(nurse=self.request.user)

class PatentProfileViewSet(viewsets.ModelViewSet):
    queryset = Observation.objects.all()
    serializer_class = PatientProfileSerializer
    permission_classes = [IsAuthenticated, IsPatient]