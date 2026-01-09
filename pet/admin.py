from django.contrib import admin
from .models import *

@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = ['name', 'species', 'breed', 'owner', 'birth_date']
    list_filter = ['species', 'owner']
    search_fields = ['name', 'species', 'breed', 'owner__username']
    readonly_fields = ['age']


@admin.register(DigitalPetPassport)
class DigitalPetPassportAdmin(admin.ModelAdmin):
    list_display = ['pet', 'vet_notes']
    search_fields = ['pet__name', 'vet_notes']


@admin.register(VaccinationRecord)
class VaccinationRecordAdmin(admin.ModelAdmin):
    list_display = ['pet', 'vaccine_name', 'vaccination_date', 'next_due_date', 'veterinarian_name']
    list_filter = ['vaccination_date', 'pet']
    search_fields = ['pet__name', 'vaccine_name', 'veterinarian_name']
    date_hierarchy = 'vaccination_date'


@admin.register(VeterinaryAppointment)
class VeterinaryAppointmentAdmin(admin.ModelAdmin):
    list_display = ['pet', 'appointment_date', 'veterinarian_name', 'clinic_name', 'reason']
    list_filter = ['appointment_date', 'pet']
    search_fields = ['pet__name', 'veterinarian_name', 'clinic_name', 'reason']
    date_hierarchy = 'appointment_date'


@admin.register(DailyCareLog)
class DailyCareLogAdmin(admin.ModelAdmin):
    list_display = ['pet', 'log_date', 'log_time', 'activity_type', 'description']
    list_filter = ['activity_type', 'log_date', 'pet']
    search_fields = ['pet__name', 'description']
    date_hierarchy = 'log_date'


@admin.register(Reminder)
class ReminderAdmin(admin.ModelAdmin):
    list_display = ['pet', 'reminder_type', 'reminder_date', 'notes']
    list_filter = ['reminder_type', 'reminder_date', 'pet']
    search_fields = ['pet__name', 'notes']
    date_hierarchy = 'reminder_date'


@admin.register(PetDocument)
class PetDocumentAdmin(admin.ModelAdmin):
    list_display = ['pet', 'description', 'document', 'uploaded_at']
    list_filter = ['uploaded_at', 'pet']
    search_fields = ['pet__name', 'description']
    date_hierarchy = 'uploaded_at'