from django.shortcuts import render
from requests import delete
from rest_framework import status,generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .models import MedicalRecord
from .serializers import MedicalRecordSerializer
from .permissions import IsDoctor

class MedicalRecordListCreateView(generics.ListCreateAPIView):
    queryset = MedicalRecord.objects.all()
    serializer_class = MedicalRecordSerializer
    permission_classes = [IsAuthenticated,IsDoctor]

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





