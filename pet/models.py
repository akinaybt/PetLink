from datetime import date

from django.conf import settings
from django.db import models
# from user.models import CustomUser

class Pet(models.Model):
    """
    Represents a pet owned by a user.
    """
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='pets'
    )
    name = models.CharField(max_length=100)
    species = models.CharField(max_length=50, help_text="e.g., Dog, Cat, Hamster")
    breed = models.CharField(max_length=50, blank=True, null=True)
    birth_date = models.DateField()

    @property
    def age(self) -> str:
        """
        Calculates the pet's age dynamically based on its birth date.
        - If the pet is under 1 year old, age is shown in months.
        - If the pet is 1 year or older, age is shown in years and months.
        """
        today = date.today()
        total_months = (today.year - self.birth_date.year) * 12 + (today.month - self.birth_date.month)

        # Adjust for the day of the month
        if today.day < self.birth_date.day:
            total_months -= 1

        if total_months < 12:
            return f"{total_months} months"
        else:
            years = total_months // 12
            months = total_months % 12
            if months == 0:
                return f"{years} years"
            return f"{years} years and {months} months"

    def __str__(self):
        return f"{self.name} ({self.species})"

class DigitalPetPassport(models.Model):
    """
    Acts as a digital passport for a single pet, containing veterinary data.
    """
    pet = models.OneToOneField(
        Pet,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='passport'
    )
    vet_notes = models.TextField(blank=True, help_text="General veterinary notes.")

    def __str__(self):
        return f"Passport for {self.pet.name}"


class VaccinationRecord(models.Model):
    """
    Represents a vaccination record for a pet.
    """
    pet = models.ForeignKey(
        Pet,
        on_delete=models.CASCADE,
        related_name='vaccinations'
    )
    vaccine_name = models.CharField(max_length=100, help_text="Name of the vaccine (e.g., Rabies, Distemper)")
    vaccination_date = models.DateField(help_text="Date when the vaccine was administered")
    next_due_date = models.DateField(blank=True, null=True, help_text="Next due date for this vaccine")
    veterinarian_name = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.vaccine_name} for {self.pet.name} on {self.vaccination_date}"

    class Meta:
        ordering = ['-vaccination_date']


class VeterinaryAppointment(models.Model):
    """
    Represents a veterinary appointment for a pet.
    """
    pet = models.ForeignKey(
        Pet,
        on_delete=models.CASCADE,
        related_name='vet_appointments'
    )
    appointment_date = models.DateTimeField(help_text="Date and time of the appointment")
    veterinarian_name = models.CharField(max_length=100)
    clinic_name = models.CharField(max_length=200, blank=True)
    reason = models.CharField(max_length=200, help_text="Reason for the visit")
    notes = models.TextField(blank=True, help_text="Additional notes about the appointment")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.pet.name} - {self.reason} on {self.appointment_date.strftime('%Y-%m-%d %H:%M')}"

    class Meta:
        ordering = ['-appointment_date']


class DailyCareLog(models.Model):
    """
    Represents a daily care activity log for a pet.
    """
    class ActivityType(models.TextChoices):
        FEEDING = 'FEED', 'Feeding'
        MEDICATION = 'MED', 'Medication'
        WALK = 'WALK', 'Walk/Exercise'
        OTHER = 'OTH', 'Other'

    pet = models.ForeignKey(
        Pet,
        on_delete=models.CASCADE,
        related_name='care_logs'
    )
    log_date = models.DateField(help_text="Date of the activity")
    log_time = models.TimeField(help_text="Time of the activity")
    activity_type = models.CharField(
        max_length=4,
        choices=ActivityType.choices,
        default=ActivityType.OTHER
    )
    description = models.TextField(help_text="Description of the activity")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.pet.name} - {self.get_activity_type_display()} on {self.log_date} at {self.log_time}"

    class Meta:
        ordering = ['-log_date', '-log_time']


class Reminder(models.Model):
    """
    Represents a reminder for a specific pet (e.g., for feeding or vet appointments).
    """
    class ReminderType(models.TextChoices):
        VACCINATION = 'VACC', 'Vaccination'
        VETERINARY = 'VET', 'Veterinary Appointment'
        FEEDING = 'FEED', 'Feeding Time'
        OTHER = 'OTH', 'Other'

    pet = models.ForeignKey(
        Pet,
        on_delete=models.CASCADE,
        related_name='reminders'
    )
    reminder_type = models.CharField(
        max_length=4,
        choices=ReminderType.choices,
        default=ReminderType.OTHER
    )
    reminder_date = models.DateTimeField()
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reminder for {self.pet.name} on {self.reminder_date.strftime('%Y-%m-%d %H:%M')}"


class PetDocument(models.Model):
    """
    Represents a document for a specific pet (e.g., receipts or medical documents).
    """
    pet = models.ForeignKey(
        Pet,
        on_delete=models.CASCADE,
        related_name='documents'
    )
    document = models.FileField(upload_to='pet_documents/')
    description = models.CharField(max_length=255, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Document for {self.pet.name} - {self.description}"