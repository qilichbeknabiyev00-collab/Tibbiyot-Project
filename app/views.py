from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.permissions import IsAuthenticated
from .permissions import IsDoctor, IsNurse, IsPatient
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from .models import MedicalRecord,User,Message
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status,generics
from rest_framework.views import APIView
from django.shortcuts import render
from django.db.models import Q
from .serializers import (
    MessageSerializer,
    PatientProfileSerializer,
    MessageForPatientSerializer,
    RegistrationSerializer,
    MedicationSerializer,
    ObservationSerializer,
    PatientSerializer,
    MedicalRecordSerializer, PrescriptionSerializer
)

class PatientProfileView(generics.RetrieveAPIView):
    serializer_class = PatientProfileSerializer
    permission_classes = [IsAuthenticated,IsPatient]


    def get_object(self):
        # Foydalanuvchi o‘z profilini oladi
        return self.request.user

class MedicalRecordListCreateView(generics.ListCreateAPIView):
    queryset = MedicalRecord.objects.all()
    serializer_class = MedicalRecordSerializer
    permission_classes = [IsAuthenticated,IsPatient]

    def perform_create(self, serializer):
        serializer.save(doctor=self.request.user)

class PrescriptionCreateView(generics.CreateAPIView):
    serializer_class = PrescriptionSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(nurse=self.request.user)

class MedicalRecordDetailView(GenericAPIView):
    queryset = MedicalRecord.objects.all()
    serializer_class = MedicalRecordSerializer

    # UPDATE
    def put(self, request, *args, **kwargs):
        record = get_object_or_404(MedicalRecord, pk=kwargs["pk"])

        serializer = MedicalRecordSerializer(
            record,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Ma'lumot yangilandi",
                "data": serializer.data
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DELETE
    def delete(self, request, *args, **kwargs):
        record = get_object_or_404(MedicalRecord, pk=kwargs["pk"])
        record.delete()

        return Response({
            "message": "Ma'lumot o‘chirildi"
        }, status=status.HTTP_200_OK)

class ObservationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MedicalRecord.objects.all()
    serializer_class = MedicalRecordSerializer
    permission_classes = [IsAuthenticated,IsNurse]

class PatientMedicalRecordListView(generics.ListAPIView):
    queryset = MedicalRecord.objects.all()
    serializer_class = MedicalRecordSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return MedicalRecord.objects.filter(patient=self.request.user)

class PatientMessageCreateView(generics.CreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsPatient]

    def perform_create(self, serializer):
        doctor_id = self.request.data.get("doctor_id")
        print("DOCTOR ID:", doctor_id)
        serializer.save(
            sender=self.request.user,
            receiver_id=doctor_id
        )

class PatientMessageListView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsPatient]
    #
    def get_messages(self, obj):
        # Patient yuborgan xabarlar
        sent = Message.objects.filter(sender=obj, receiver=obj.assigned_doctor)
        # Doctor yuborgan xabarlar
        received = Message.objects.filter(sender=obj.assigned_doctor, receiver=obj)
        # ikkala querysetni birlashtirish va tartiblash
        all_msgs = sorted(
            list(sent) + list(received),
            key=lambda m: m.created_at,
            reverse=True
        )
        return MessageForPatientSerializer(all_msgs, many=True).data

class RegisterView(generics.CreateAPIView):
    serializer_class = RegistrationSerializer
    permission_classes = [AllowAny]

class DoctorMessageListView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Message.objects.filter(receiver=self.request.user)

class MessageListView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsDoctor]

    def get_queryset(self):
        return Message.objects.filter(
            Q(sender=self.request.user) |
            Q(receiver=self.request.user)
        ).order_by("-created_at")

class DoctorReplyMessageView(generics.CreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        patient_id = self.request.data.get("patient_id")

        print("PATIENT ID:", patient_id)
        serializer.save(
            sender=self.request.user,
            receiver_id=patient_id
        )

class PatientListView(generics.ListAPIView):
    queryset = User.objects.filter(role='Patient')
    serializer_class = PatientSerializer
    Permission_classes = [IsAuthenticated,IsNurse]

class MedicationCreateView(generics.CreateAPIView):
    serializer_class = MedicationSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(nurse=self.request.user)

class MedicationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MedicalRecord.objects.all()
    serializer_class = MedicalRecordSerializer
    permission_classes = [IsAuthenticated]

class ObservationCreateView(generics.CreateAPIView):
    serializer_class = ObservationSerializer
    permission_classes = [IsAuthenticated,IsNurse]