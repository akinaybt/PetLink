from rest_framework import serializers
from .models import Pet, Medication, Feeding, Walk


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

class WalkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Walk
        fields = ['id', 'pet', 'date', 'time', 'notes']