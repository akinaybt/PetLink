from datetime import date

from django.conf import settings
from django.db import models

class Pet(models.Model):
    """
    Represents a pet owned by a user.
    """
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='pets'
    )
    photo = models.ImageField(upload_to='pets_photo/', blank=True)

    name = models.CharField(max_length=100)
    species = models.CharField(max_length=50, help_text="e.g., Dog, Cat, Hamster")
    breed = models.CharField(max_length=50, blank=True, null=True)
    birth_date = models.DateField()

    class Meta:
        verbose_name = 'Pet'
        verbose_name_plural = 'Pets'

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

class Appointment(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='appointments')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    appointment_date = models.DateField()
    appointment_time = models.TimeField()

    class Meta:
        verbose_name = 'Appointment'
        verbose_name_plural = 'Appointments'

    def __str__(self):
        return f"Appointment for {self.pet.name} on {self.appointment_date.strftime('%d-%m-%Y')} at {self.appointment_time.strftime('%H:%M')}"


class BaseActivity(models.Model):
    """
    Абстрактная модель для хранения общих данных об активности.
    """
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='activities')  # Связь с питомцем
    date = models.DateField(null=False, blank=False)  # Дата активности
    time = models.TimeField(null=False, blank=False)  # Время активности
    notes = models.TextField(blank=True)  # Заметки
    created_at = models.DateTimeField(auto_now_add=True)  # Дата создания записи
    updated_at = models.DateTimeField(auto_now=True)  # Дата последнего обновления

    class Meta:
        abstract = True  # Базовая модель, не создаёт таблицу в базе данных

class Medication(BaseActivity):
    """
    Модель для учёта медицинских процедур и препаратов.
    """
    pet = models.ForeignKey('Pet', on_delete=models.CASCADE, related_name='medications')  # Уникальное related_name
    medication_name = models.CharField(max_length=100)  # Название препарата
    dosage = models.CharField(max_length=50)  # Дозировка
    frequency = models.IntegerField(default=1)  # Как часто нужно принимать (количество раз в день)

    def __str__(self):
        return f"{self.medication_name} для {self.pet.name} ({self.date})"


class Feeding(BaseActivity):
    """
    Модель для учёта кормления питомца.
    """
    pet = models.ForeignKey('Pet', on_delete=models.CASCADE, related_name='feedings')  # Уникальное related_name
    food_type = models.CharField(max_length=100)  # Тип корма
    amount = models.CharField(max_length=50)  # Количество

    def __str__(self):
        return f"{self.food_type} ({self.amount}) для {self.pet.name} ({self.date})"


class Walk(BaseActivity):
    """
    Модель для учёта прогулок.
    """
    pet = models.ForeignKey('Pet', on_delete=models.CASCADE, related_name='walks')  # Уникальное related_name

    def __str__(self):
        return f"Прогулка с {self.pet.name} ({self.date})"