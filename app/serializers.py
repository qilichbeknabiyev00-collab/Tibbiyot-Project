from rest_framework import serializers
from .models import User, MedicalRecord, Medication, Observation, Message

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'role')

class MedicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medication
        fields = ('id', 'name', 'dosage', 'notes'),
        read_only_fields = ["nurse", "given_at"]

class MedicalRecordSerializer(serializers.ModelSerializer):
    doctor_name = serializers.CharField(source="doctor.username", read_only=True)
    role = serializers.CharField(source="role.name", read_only=True)
    class Meta:
        model = MedicalRecord
        fields = ['id', 'patient', 'doctor','doctor_name' ,'role','diagnosis', 'treatment_plan', 'created_at', 'updated_at']
        read_only_fields = ['doctor','role', 'created_at', 'updated_at']

class ObservationSerializer(serializers.ModelSerializer):
    medications = MedicalRecordSerializer(many=True, read_only=True)

    class Meta:
        model = Observation
        fields = ('id', 'patient', 'nurse', 'temperature', 'blood_pressure', 'notes', 'created_at')
        read_only_fields = ["nurse", "created_at"]

class StatisticsSerializer(serializers.Serializer):
    total_patients = serializers.IntegerField()
    total_doctors = serializers.IntegerField()
    total_records = serializers.IntegerField()
    total_commands_diagnosed = serializers.CharField()

class TreatmentSuggestionSerializer(serializers.Serializer):
    diagnosis = serializers.CharField()
    suggested_treatment = serializers.CharField()

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'
        read_only_fields = ["sender", "receiver"]

class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "role"]

class MessageForPatientSerializer(serializers.ModelSerializer):
    sender = serializers.StringRelatedField()
    receiver = serializers.StringRelatedField()

    class Meta:
        model = Message
        fields = ['id', 'text', 'created_at', 'sender', 'receiver']
# Patient medical recordlarini ko‘rsatish

class MedicalRecordForPatientSerializer(serializers.ModelSerializer):
    doctor = DoctorSerializer(read_only=True)

    class Meta:
        model = MedicalRecord
        fields = ["id", "diagnosis", "treatment_plan", "doctor", "created_at", "updated_at"]

# Patient Profile serializer
class PatientProfileSerializer(serializers.ModelSerializer):
    assigned_doctor = DoctorSerializer(read_only=True)
    messages = serializers.SerializerMethodField()
    medical_records = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username','email', 'role', 'assigned_doctor', 'messages', 'medical_records']

    def get_messages(self, obj):
        if not obj.assigned_doctor:
            return []
        doctor = obj.assigned_doctor
        sent = Message.objects.filter(sender=obj, receiver=doctor)
        received = Message.objects.filter(sender=doctor, receiver=obj)
        all_msgs = list(sent) + list(received)
        all_msgs.sort(key=lambda m: m.created_at, reverse=True)
        return MessageForPatientSerializer(all_msgs, many=True).data

    def get_medical_records(self, obj):
        return MedicalRecordForPatientSerializer(obj.medical_records.all(), many=True).data

class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = [ "username", "password", 'role']

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            role=validated_data['role']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class PatientSerializer(serializers.ModelSerializer):
    medical_records = MedicalRecordSerializer(many=True, read_only=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'email','role','medical_records']
