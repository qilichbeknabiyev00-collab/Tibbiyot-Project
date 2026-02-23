from django.shortcuts import render
from rest_framework import viewsets,status
from rest_framework.response import Response
from .utils import suggest_treatment
from collections import Counter
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .models import MedicalRecord, Observation, PatientProfile, User
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

class StatisticsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        total_patients = User.objects.filter(role= 'Patient').count()
        total_doctors = User.objects.filter(role= 'Doctor').count()
        total_records = MedicalRecord.objects.count()

        diagnoses = MedicalRecord.objects.values_list('diagnosis', flat=True ).distinct()
        most_comman = Counter(diagnoses).most_comman(1)
        most_common_diagnosis = most_comman[0][0] if most_comman else "No records"

        data = {
            "total_patients": total_patients,
            "total_doctors": total_doctors,
            "total_records": total_records,
            "most_common_diagnosis": most_common_diagnosis
        }
        return Response(data)

@api_view(['Post'])
def treatment_suggestion(request):
    diagnosis = request.data['diagnosis']
    if not diagnosis:
        return Response({"error":"Diagnosis is required"}), status.HTTP_400_BAD_REQUEST
    suggestion = suggest_treatment(diagnosis)
    return Response({
        "diagnosis": diagnosis,
        "suggested_treatment": suggestion
    })