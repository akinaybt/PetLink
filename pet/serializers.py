from rest_framework import serializers
from .models import Pet, DigitalPetPassport, Reminder, PetDocument

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
    age = serializers.CharField(source='age', read_only=True)
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


class ReminderSerializer(serializers.ModelSerializer):
    """
    Serializer for the Reminder model. It ensures that users can only
    assign reminders to pets they own.
    """
    class Meta:
        model = Reminder
        fields = ['id', 'pet', 'reminder_type', 'reminder_date', 'notes', 'created_at']

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
    class Meta:
        model = PetDocument
        fields = ['id', 'pet', 'document', 'description', 'uploaded_at']
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
