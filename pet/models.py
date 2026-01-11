from datetime import date

from django.conf import settings
from django.db import models

class Pet(models.Model):
    """
    Represents a pet owned by a user.

    This class serves as a model for storing pet-related information, such as
    its owner, photo, name, species, breed, and birth date. It provides a
    dynamic property for calculating the pet's age based on its birth date.

    :ivar owner: The user who owns the pet.
    :type owner: ForeignKey
    :ivar photo: An optional photo of the pet.
    :type photo: ImageField
    :ivar name: The name of the pet.
    :type name: CharField
    :ivar species: The species of the pet (e.g., Dog, Cat, Hamster).
    :type species: CharField
    :ivar breed: The breed of the pet, which can be blank or null.
    :type breed: CharField
    :ivar birth_date: The pet's date of birth.
    :type birth_date: DateField
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
    """
        Represents an appointment for a pet.

        The Appointment model is used to store details about a scheduled appointment
        for a pet. Each appointment is associated with a specific pet and contains
        information such as the appointment's name, description, date, and time.
        This model allows easy management and retrieval of pet appointments.

        :ivar pet: The pet associated with the appointment.
        :type pet: ForeignKey
        :ivar name: The name of the appointment.
        :type name: str
        :ivar description: An optional description of the appointment.
        :type description: str
        :ivar appointment_date: The date on which the appointment is scheduled.
        :type appointment_date: date
        :ivar appointment_time: The time at which the appointment is scheduled.
        :type appointment_time: time
        """
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
    Base model representing a generic activity log associated with a pet.

    This class provides a foundation for defining pet-related activities, including tracking the date,
    time, and optional notes for a specific activity. It includes metadata for creation and
    modification timestamps and enforces relationships with a `Pet` instance. This is an abstract
    model and does not create a corresponding database table.

    :ivar pet: Reference to the related pet instance.
    :type pet: ForeignKey(Pet)
    :ivar date: Date of the activity.
    :type date: DateField
    :ivar time: Time of the activity.
    :type time: TimeField
    :ivar notes: Additional information or notes related to the activity (optional).
    :type notes: TextField
    :ivar created_at: Timestamp indicating when the record was created.
    :type created_at: DateTimeField
    :ivar updated_at: Timestamp indicating the last time the record was updated.
    :type updated_at: DateTimeField
    """
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='activities')  # Связь с питомцем
    date = models.DateField(null=False, blank=False)  # Дата активности
    time = models.TimeField(null=False, blank=False)  # Время активности
    notes = models.TextField(blank=True)  # Заметки
    created_at = models.DateTimeField(auto_now_add=True)  # Дата создания записи
    updated_at = models.DateTimeField(auto_now=True)  # Дата последнего обновления

    class Meta:
        abstract = True  # Базовая модель, не создаёт таблицу в базе данных

    def __str__(self):
        return f"{self.day} for activity id {self.activity_log.id}"

class Medication(BaseActivity):
    """
    Represents a medication associated with a pet's treatment plan.

    This class extends BaseActivity and is used to manage information
    about a specific medication prescribed for a pet. The purpose of this
    class is to store details about the medication name, dosage, and
    frequency of administration for each pet.

    :ivar pet: The pet to which the medication record belongs.
    :type pet: ForeignKey
    :ivar medication_name: The name of the prescribed medication.
    :type medication_name: CharField
    :ivar dosage: The dosage of the prescribed medication.
    :type dosage: CharField
    :ivar frequency: The number of times the medication should be given
        daily. Defaults to 1.
    :type frequency: IntegerField
    """
    pet = models.ForeignKey('Pet', on_delete=models.CASCADE, related_name='medications')  # Уникальное related_name
    medication_name = models.CharField(max_length=100)  # Название препарата
    dosage = models.CharField(max_length=50)  # Дозировка
    frequency = models.IntegerField(default=1)  # Как часто нужно принимать (количество раз в день)

    def __str__(self):
        return f"{self.medication_name} для {self.pet.name} ({self.date})"


class Feeding(BaseActivity):
    """
    Represents the Feeding activity for pets.

    This class maintains information about the feeding activities of pets, including
    the type of food, the amount of food provided, and the associated pet. It is designed
    to track and manage feeding records.

    :ivar pet: The pet associated with this feeding activity.
    :type pet: models.ForeignKey
    :ivar food_type: The type of food used during the feeding.
    :type food_type: str
    :ivar amount: The amount of food provided during the feeding.
    :type amount: str
    """
    pet = models.ForeignKey('Pet', on_delete=models.CASCADE, related_name='feedings')  # Уникальное related_name
    food_type = models.CharField(max_length=100)  # Тип корма
    amount = models.CharField(max_length=50)  # Количество

    def __str__(self):
        return f"{self.food_type} ({self.amount}) для {self.pet.name} ({self.date})"


class Walk(BaseActivity):
    """
    Represents a walk activity associated with a pet.

    This class is a type of activity that records a walk taken with a specific pet.
    Each walk is tied to a particular pet instance and is intended to store
    information regarding the pet's walks. The class inherits from a base class
    `BaseActivity` which might define shared attributes or behaviors for various
    activities.

    :ivar pet: The pet associated with the walk. This relationship is unique as it
        uses a specific ``related_name`` for linking to the pet's walks.
    :type pet: models.ForeignKey
    """
    pet = models.ForeignKey('Pet', on_delete=models.CASCADE, related_name='walks')  # Уникальное related_name

    def __str__(self):
        return f"Прогулка с {self.pet.name} ({self.date})"


class PetDocument(models.Model):
    """
    Represents a document associated with a pet.

    This model allows the association of various types of documents
    (e.g., medical records, vaccination records, insurances) with a
    pet instance. It provides a structured way to store and manage
    pet-related documentation.

    :ivar pet: The pet to which the document is linked. This is a
        foreign key referencing the 'Pet' model.
    :type pet: ForeignKey
    :ivar file: The uploaded file for the pet document.
    :type file: FileField
    :ivar title: The descriptive title of the pet document.
    :type title: CharField
    :ivar document_type: The type of document. It can be one of the
        predefined choices (e.g., 'passport', 'vaccination').
    :type document_type: CharField
    :ivar uploaded_at: The timestamp indicating when the document was uploaded.
    :type uploaded_at: DateTimeField
    """
    pet = models.ForeignKey(
        Pet,
        on_delete=models.CASCADE,
        related_name="documents"
    )

    file = models.FileField(upload_to="pet_documents/")
    title = models.CharField(
        max_length=150,
        help_text="For example: VET passport, Blood test, Vaccination"
    )

    document_type = models.CharField(
        max_length=50,
        choices=[
            ("passport", "Passport"),
            ("vaccination", "Vaccination"),
            ("analysis", "Medical Analysis"),
            ("insurance", "Insurance"),
            ("other", "Other"),
        ],
        default="other"
    )

    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Pet Document"
        verbose_name_plural = "Pet Documents"
        ordering = ["-uploaded_at"]

    def str(self):
        return f"{self.title} – {self.pet.name}"