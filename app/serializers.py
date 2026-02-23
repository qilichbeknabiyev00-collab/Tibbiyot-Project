from rest_framework import serializers
from .models import User, PatientProfile, MedicalRecord, Medication, Observation

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'role')

class PatientProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = PatientProfile
        fields = '__all__'

class MedicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medication
        fields = ('id', 'name', 'dosage', 'notes')

class MedicalRecordSerializer(serializers.ModelSerializer):
    medications = MedicationSerializer(many=True, read_only=True)
    doctor = UserSerializer(read_only=True)
    class Meta:
        model = MedicalRecord
        fields = ('id', 'doctor', 'diagnosis', 'treatment_plan', 'created_at', 'updated_at', 'medications')


class ObservationSerializer(serializers.ModelSerializer):
    medications = MedicalRecordSerializer(many=True, read_only=True)

    class Meta:
        model = Observation
        fields = ('id', 'patient', 'nurse', 'temperature', 'blood_pressure', 'notes', 'created_at')


class StatisticsSerializer(serializers.Serializer):
    total_patients = serializers.IntegerField()
    total_doctors = serializers.IntegerField()
    total_records = serializers.IntegerField()
    total_commands_diagnosed = serializers.CharField()

class TreatmentSuggestionSerializer(serializers.Serializer):
    diagnosis = serializers.CharField()
    suggested_treatment = serializers.CharField()