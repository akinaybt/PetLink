from rest_framework import serializers
from .models import Pet, DigitalPetPassport, Reminder, PetDocument, VaccinationRecord, VeterinaryAppointment, DailyCareLog

class DigitalPetPassportSerializer(serializers.ModelSerializer):
    """
    Serializer for the DigitalPetPassport model.
    """
    class Meta:
        model = DigitalPetPassport
        fields = ['vet_notes']


class PetSerializer(serializers.ModelSerializer):
    """
    Serializer for the Pet model. It handles nested creation of the
    DigitalPetPassport and enforces the 5-pet limit per user.
    """
    owner = serializers.ReadOnlyField(source='owner.username')
    age = serializers.CharField(read_only=True)
    passport = DigitalPetPassportSerializer()

    class Meta:
        model = Pet
        fields = ['id', 'owner', 'name', 'species', 'breed', 'birth_date', 'age', 'passport']

    def validate(self, data):
        """
        Check that the user does not create more than 5 pets.
        This validation is only triggered on POST requests.
        """
        request = self.context.get('request')
        if request and request.method == 'POST':
            if request.user.pets.count() >= 5:
                raise serializers.ValidationError("You have reached the maximum limit of 5 pets.")
        return data

    def create(self, validated_data):
        """
        Create a new Pet and its associated DigitalPetPassport.
        """
        passport_data = validated_data.pop('passport')
        pet = Pet.objects.create(**validated_data)
        DigitalPetPassport.objects.create(pet=pet, **passport_data)
        return pet

    def update(self, instance, validated_data):
        """
        Update an existing Pet and its associated DigitalPetPassport.
        """
        passport_data = validated_data.pop('passport', None)
        if passport_data:
            # Update the nested passport object
            passport_serializer = self.fields['passport']
            passport_instance = instance.passport
            passport_serializer.update(passport_instance, passport_data)

        # Update the pet instance
        return super().update(instance, validated_data)


class VaccinationRecordSerializer(serializers.ModelSerializer):
    """
    Serializer for the VaccinationRecord model.
    """
    pet_name = serializers.CharField(source='pet.name', read_only=True)

    class Meta:
        model = VaccinationRecord
        fields = ['id', 'pet', 'pet_name', 'vaccine_name', 'vaccination_date', 'next_due_date', 
                  'veterinarian_name', 'notes', 'created_at']
        read_only_fields = ['created_at']

    def __init__(self, *args, **kwargs):
        """
        Filter the 'pet' field queryset to only include pets owned by the
        current user.
        """
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and hasattr(request, "user"):
            self.fields['pet'].queryset = Pet.objects.filter(owner=request.user)


class VeterinaryAppointmentSerializer(serializers.ModelSerializer):
    """
    Serializer for the VeterinaryAppointment model.
    """
    pet_name = serializers.CharField(source='pet.name', read_only=True)

    class Meta:
        model = VeterinaryAppointment
        fields = ['id', 'pet', 'pet_name', 'appointment_date', 'veterinarian_name', 
                  'clinic_name', 'reason', 'notes', 'created_at']
        read_only_fields = ['created_at']

    def __init__(self, *args, **kwargs):
        """
        Filter the 'pet' field queryset to only include pets owned by the
        current user.
        """
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and hasattr(request, "user"):
            self.fields['pet'].queryset = Pet.objects.filter(owner=request.user)


class DailyCareLogSerializer(serializers.ModelSerializer):
    """
    Serializer for the DailyCareLog model.
    """
    pet_name = serializers.CharField(source='pet.name', read_only=True)
    activity_type_display = serializers.CharField(source='get_activity_type_display', read_only=True)

    class Meta:
        model = DailyCareLog
        fields = ['id', 'pet', 'pet_name', 'log_date', 'log_time', 'activity_type', 
                  'activity_type_display', 'description', 'created_at']
        read_only_fields = ['created_at']

    def __init__(self, *args, **kwargs):
        """
        Filter the 'pet' field queryset to only include pets owned by the
        current user.
        """
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and hasattr(request, "user"):
            self.fields['pet'].queryset = Pet.objects.filter(owner=request.user)


class ReminderSerializer(serializers.ModelSerializer):
    """
    Serializer for the Reminder model. It ensures that users can only
    assign reminders to pets they own.
    """
    pet_name = serializers.CharField(source='pet.name', read_only=True)
    reminder_type_display = serializers.CharField(source='get_reminder_type_display', read_only=True)

    class Meta:
        model = Reminder
        fields = ['id', 'pet', 'pet_name', 'reminder_type', 'reminder_type_display', 
                  'reminder_date', 'notes', 'created_at']
        read_only_fields = ['created_at']

    def __init__(self, *args, **kwargs):
        """
        Filter the 'pet' field queryset to only include pets owned by the
        current user, preventing users from creating reminders for other's pets.
        """
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and hasattr(request, "user"):
            self.fields['pet'].queryset = Pet.objects.filter(owner=request.user)

class PetDocumentSerializer(serializers.ModelSerializer):
    """
    Serializer for the PetDocument model.
    """
    pet_name = serializers.CharField(source='pet.name', read_only=True)

    class Meta:
        model = PetDocument
        fields = ['id', 'pet', 'pet_name', 'document', 'description', 'uploaded_at']
        read_only_fields = ['uploaded_at']

    def __init__(self, *args, **kwargs):
        """
        Filter the 'pet' field queryset to only include pets owned by the
        current user.
        """
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and hasattr(request, "user"):
            self.fields['pet'].queryset = Pet.objects.filter(owner=request.user)
