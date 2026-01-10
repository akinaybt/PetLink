from rest_framework import serializers
from .models import Pet, Medication, Feeding, Walk, Appointment, PetDocument


class PetSerializer(serializers.ModelSerializer):
    owner_name= serializers.SerializerMethodField()

    class Meta:
        model = Pet
        fields = ['id', 'photo', 'name', 'species', 'breed', 'birth_date', 'age',
                  'owner_name']  # owner будет возвращаться в ответах
        extra_kwargs = {
            'owner': {'read_only': True}  # Поле owner доступно только для чтения
        }

    def get_owner_name(self, obj):
        return obj.owner.first_name if obj.owner else None

class MedicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medication
        fields = ['id', 'pet', 'date', 'time', 'notes', 'medication_name', 'dosage', 'frequency']

class FeedingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feeding
        fields = ['id', 'pet', 'date', 'time', 'notes', 'food_type', 'amount']
        extra_kwargs = {
            'id': {'read_only': True},  # ID должно быть только для чтения
        }

    def create(self, validated_data):
        if 'custom_field' in validated_data:  # Если дополнительное поле передаётся
            validated_data.pop('custom_field')  # Удалите его
        return Feeding.objects.create(**validated_data)

class WalkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Walk
        fields = ['id', 'pet', 'date', 'time', 'notes']

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['id', 'pet', 'name', 'appointment_date', 'appointment_time']

class PetDocumentSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели PetDocument.
    """
    class Meta:
        model = PetDocument
        fields = ['id', 'pet', 'file', 'title', 'document_type', 'uploaded_at']
        read_only_fields = ['uploaded_at']