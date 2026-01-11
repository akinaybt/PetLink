from rest_framework import serializers
from .models import Pet, Medication, Feeding, Walk, Appointment, PetDocument


class PetSerializer(serializers.ModelSerializer):
    """
    Serializes Pet model instances.

    This serializer is responsible for serializing and deserializing Pet model
    instances to and from representations such as JSON. It defines the fields
    that are included in the serialization process and specifies the model it
    is based on. It is built using Django REST framework's `ModelSerializer`.

    """
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
    """
    Serializes Medication model instances.

    This serializer is responsible for serializing and deserializing Medication model
    instances to and from representations such as JSON. It defines the fields
    that are included in the serialization process and specifies the model it
    is based on. It is built using Django REST framework's `ModelSerializer`.
    """
    class Meta:
        model = Medication
        fields = ['id', 'pet', 'date', 'time', 'notes', 'medication_name', 'dosage', 'frequency']

class FeedingSerializer(serializers.ModelSerializer):
    """
    Serializes Feeding model instances.

    This serializer is responsible for serializing and deserializing Feeding model
    instances to and from representations such as JSON. It defines the fields
    that are included in the serialization process and specifies the model it
    is based on. It is built using Django REST framework's `ModelSerializer`.

    """
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
    """
    Serializer class for Walk model.

    This serializer is responsible for serializing and deserializing Walk model
    instances to and from representations such as JSON. It defines the fields
    that are included in the serialization process and specifies the model it
    is based on. It is built using Django REST framework's `ModelSerializer`.
    """
    class Meta:
        model = Walk
        fields = ['id', 'pet', 'date', 'time', 'notes']

class AppointmentSerializer(serializers.ModelSerializer):
    """
    Handles the serialization and deserialization of Appointment model instances.

    Provides a way to transform Appointment model instances into serializable
    representations such as JSON. Useful for API serialization
    and ensuring data integrity.
    """
    class Meta:
        model = Appointment
        fields = ['id', 'pet', 'name', 'appointment_date', 'appointment_time']

class PetDocumentSerializer(serializers.ModelSerializer):
    """
    Serializer for PetDocument model.

    This class is a Django REST Framework serializer for the `PetDocument` model,
    providing serialization and deserialization of the model's fields. It defines
    the fields to include in the serialized representation and specifies which
    fields are read-only. The serializer helps in managing and validating data
    during input and output operations for `PetDocument` instances.
    """
    class Meta:
        model = PetDocument
        fields = ['id', 'pet', 'file', 'title', 'document_type', 'uploaded_at']
        read_only_fields = ['uploaded_at']