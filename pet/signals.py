from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from django.http import BadHeaderError
from django.utils.timezone import now
from datetime import datetime, timedelta
from django.utils.timezone import make_aware, now
from .models import Medication, Feeding, Walk, Appointment

@receiver(post_save, sender=Medication)
def send_medication_reminder(sender, instance, created, **kwargs):
    """
    Отправка напоминания для Medication после сохранения.
    """
    if created:
        # Рассчитать время напоминания: за 2 часа до указанного времени
        reminder_time = datetime.combine(instance.date, instance.time) - timedelta(hours=2)

    # Проверяем: напоминание только для событий в будущем
        if reminder_time > now():
            send_notification(
                instance.pet.owner.email,
            f"Напоминание: Лечение {instance.medication_name}",
            f"Дайте питомцу препарат {instance.medication_name} {instance.dosage} за 2 часа до лечения."
        )


@receiver(post_save, sender=Feeding)
def send_feeding_reminder(sender, instance, created, **kwargs):
    """
    Отправка напоминания для Feeding после сохранения.
    """
    if created:
        reminder_time = datetime.combine(instance.date, instance.time) - timedelta(minutes=1)

        if not reminder_time.tzinfo:  # Проверяем, имеет ли сохранённое время информацию о временной зоне
            reminder_time = make_aware(reminder_time)

        if reminder_time > now():
            send_notification(
                instance.pet.owner.email,
                f"Напоминание: Кормление {instance.food_type}",
                f"Не забудьте покормить питомца {instance.pet.name}. Тип корма: {instance.food_type}, Количество: {instance.amount}."
            )


@receiver(post_save, sender=Walk)
def send_walk_reminder(sender, instance, **kwargs):
    """
    Отправка напоминания для Walk после сохранения.
    """
    reminder_time = datetime.combine(instance.date, instance.time) - timedelta(hours=2)
    if reminder_time > now():
        send_notification(
            instance.pet.owner.email,
            f"Напоминание о прогулке с {instance.pet.name}",
            f"Прогулка запланирована на {instance.date} в {instance.time}. Не забудьте подготовить место: {instance.notes}." if instance.notes else "Прогулка запланирована."
        )


@receiver(post_save, sender=Appointment)
def send_appointment_reminder(sender, instance, **kwargs):
    """
    Отправка напоминания для Appointment после сохранения.
    """
    reminder_time = datetime.combine(instance.appointment_date, instance.appointment_time) - timedelta(hours=2)
    if reminder_time > now():
        send_notification(
            instance.pet.owner.email,
            f"Напоминание: {instance.name}",
            f"Визит к ветеринару запланирован на {instance.appointment_date.strftime('%d-%m-%Y')} в {instance.appointment_time.strftime('%H:%M')}.\nПодробности: {instance.description}."
        )


def send_notification(subject, message, recipient_email):
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL, # Отправитель
            [recipient_email], # Получатель
            fail_silently=False, # Вызывать исключение, если ошибка
        )
    except BadHeaderError:
        print("Invalid header")
    except ConnectionRefusedError:
        print("Failed to connect to the email server.")
    except Exception as e:
        print(f"An error occurred: {e}")