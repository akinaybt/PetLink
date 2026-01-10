from celery import shared_task
from django.core.mail import send_mail
from datetime import datetime

@shared_task
def send_reminder(activity_type, activity_id):
    """
    Отправка напоминания для активности или приёма.
    """
    from .models import Medication, Feeding, Walk, Appointment

    # Сопоставление типов активности с моделями
    model_map = {
        'medication': Medication,
        'feeding': Feeding,
        'walk': Walk,
        'appointment': Appointment,
    }

    activity = model_map[activity_type].objects.get(id=activity_id)

    # Формирование сообщения
    subject = f"Напоминание: {activity_type.capitalize()} для питомца {activity.pet.name}"
    message = f"""
    Питомец: {activity.pet.name if hasattr(activity, 'pet') else 'N/A'}
    Дата: {activity.date if hasattr(activity, 'date') else activity.appointment_date}
    Время: {activity.time if hasattr(activity, 'time') else activity.appointment_time}
    Заметки: {activity.notes if hasattr(activity, 'notes') else activity.description}
    """

    # Отправка email (пример, замените на пуш-уведомления если требуется)
    send_mail(
        subject,
        message,
        'PetLink@gmail.com',  # Отправитель
        ['user_email@example.com'],  # Получатель
        fail_silently=False,
    )