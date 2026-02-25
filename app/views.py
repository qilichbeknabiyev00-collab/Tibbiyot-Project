from django.shortcuts import render
from requests import delete
from rest_framework import status,generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .serializers import MessageSerializer, PatientProfileSerializer, MessageForPatientSerializer, \
    RegistrationSerializer
from .models import Message


from .models import MedicalRecord,User
from .serializers import MedicalRecordSerializer, UserSerializer
from .permissions import IsDoctor, IsNurse, IsPatient


class PatientProfileView(generics.RetrieveAPIView):
    serializer_class = PatientProfileSerializer
    permission_classes = [IsAuthenticated, IsPatient]


    def get_object(self):
        return self.request.user

class MedicalRecordListCreateView(generics.ListCreateAPIView):
    queryset = MedicalRecord.objects.all()
    serializer_class = MedicalRecordSerializer
    permission_classes = [IsAuthenticated,IsPatient]

    def perform_create(self, serializer):
        serializer.save(doctor=self.request.user)


class MedicalRecordDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MedicalRecord.objects.all()
    serializer_class = MedicalRecordSerializer
    permission_classes = [IsAuthenticated,IsDoctor]

    def perform_update(self, serializer):
        serializer.save(doctor=self.request.user)

    def delete(self,request,pk):
        try:
            MedicalRecord.objects.get(pk=pk)
            record = delete()
            return Response({
                'Malumotlar o`chirildi':status.HTTP_204_NO_CONTENT,
            })
        except MedicalRecord.DoesNotExist:
            return Response({
                'error':'Topilamdi'},
                status=status.HTTP_404_NOT_FOUND
            )

    def put(self, request, pk):
        try:
            record = MedicalRecord.objects.get(pk=pk)
        except MedicalRecord.DoesNotExist:
            return Response({"error": "Topilmadi"}, status=404)

        serializer = MedicalRecordSerializer(
            record,  # instance
            data=request.data  # MUHIM!!!
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({
            "message": "Ma'lumot yangilandi",
            "data": serializer.data
        })


class PatientListView(generics.ListAPIView):
    queryset = User.objects.filter(role="patient")
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsNurse, IsDoctor]

class MedicationListCreateView(generics.ListCreateAPIView):
    queryset = MedicalRecord.objects.all()
    serializer_class = MedicalRecordSerializer
    permission_classes = [IsAuthenticated,IsNurse]

    def perform_create(self, serializer):
        serializer.save(nurse=self.request.user)


class MedicationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MedicalRecord.objects.all()
    serializer_class = MedicalRecordSerializer
    permission_classes = [IsAuthenticated,IsNurse]


class ObservationListCreateView(generics.ListCreateAPIView):
    queryset = MedicalRecord.objects.all()
    serializer_class = MedicalRecordSerializer
    permission_classes = [IsAuthenticated,IsNurse]

    def perform_create(self, serializer):
        serializer.save(nurse=self.request.user)


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


from django.db.models import Q
from django.shortcuts import get_object_or_404

class DoctorMessageListView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated,IsDoctor]

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
    permission_classes = [IsAuthenticated, IsDoctor]

    def perform_create(self, serializer):
        patient_id = self.request.data.get("patient_id")

        print("PATIENT ID:", patient_id)
        serializer.save(
            sender=self.request.user,
            receiver_id=patient_id
        )