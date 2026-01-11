from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework import permissions, status, viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Pet, Medication, Feeding, Walk, Appointment, PetDocument
from .serializers import (
    PetSerializer, MedicationSerializer, FeedingSerializer,
    WalkSerializer, AppointmentSerializer, PetDocumentSerializer
)



class PetCreateView(ListCreateAPIView):
    """
    Provides functionality for listing and creating pet profiles.

    This class-based view allows authenticated users to list and create profiles
    for their pets. Regular users can view and manage only their own pet profiles,
    while administrative users have access to see all pet profiles. The creation
    process is limited to a maximum of 5 pet profiles per user.
    """
    serializer_class = PetSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Ограничивает список питомцев только для текущего пользователя.
        """
        if self.request.user.is_staff:
            return Pet.objects.all()  # Администратор видит всех питомцев
        return Pet.objects.filter(owner=self.request.user)  # Пользователи видят только своих питомцев

    def perform_create(self, serializer):
        """
        Устанавливает владельцем текущего пользователя при создании профиля питомца.
        Ограничивает создание профилей до 5 питомцев.
        """
        # Проверка на количество профилей питомцев
        pet_count = Pet.objects.filter(owner=self.request.user).count()
        if pet_count >= 5:
            return Response(
                {"error": "You can not create more than 5 pets profiles."},
                status=status.HTTP_403_FORBIDDEN
            )

        # Создаём профиль питомца
        serializer.save(owner=self.request.user)

class MedicationView(ListCreateAPIView):
    """
    Handles the listing and creation of Medication objects for the logged-in user.

    This class enables the retrieval of Medication objects associated with the pets
    belonging to the currently authenticated user. It also allows the creation of
    new Medication objects and associates them with the user.
    """
    serializer_class = MedicationSerializer

    def get_queryset(self):
        return Medication.objects.filter(pet__owner=self.request.user)

    def perform_create(self, serializer):
        medication = serializer.save()

class FeedingView(ListCreateAPIView):
    """
    Handles the creation and retrieval of feeding records associated with pets.

    This view provides functionality to create new feeding records and retrieve a
    list of feeding records filtered by the current user's pets. The view ensures
    that users can only access feeding records related to their own pets.
    """
    serializer_class = FeedingSerializer

    def get_queryset(self):
        return Feeding.objects.filter(pet__owner=self.request.user)

    def perform_create(self, serializer):
        activity = serializer.save()

class WalkView(ListCreateAPIView):
    """
    Handles the list and creation of Walk objects specific to the logged-in user.

    This class-based view is designed to manage Walk objects by allowing users to
    retrieve a list of their walk instances or create new ones. It ensures that the
    views are tied to the authenticated user by filtering the Walk objects by the
    current user.
    """
    serializer_class = WalkSerializer

    def get_queryset(self):
        return Walk.objects.filter(pet__owner=self.request.user)

    def perform_create(self, serializer):
        walk = serializer.save()

class AppointmentView(ListCreateAPIView):
    """
    Handles creation and retrieval of appointment data for the authenticated user.

    This class-based view enables the creation and listing of appointments through
    appropriate HTTP methods. It restricts the displayed appointments to those
    associated with the pets of the currently authenticated user.
    """
    serializer_class = AppointmentSerializer

    def get_queryset(self):
        return Appointment.objects.filter(pet__owner=self.request.user)


class PetDocumentView(ListCreateAPIView):
    """
    API view for creating and retrieving pet documents.

    This class provides functionality to list and create documents associated with a
    specific pet. It filters documents based on the provided pet ID and ensures that
    the created documents are linked to the specified pet.    """
    serializer_class = PetDocumentSerializer

    def get_queryset(self):
        pet_id = self.kwargs['pet_id']
        return PetDocument.objects.filter(pet_id=pet_id)

    def perform_create(self, serializer):
        pet_id = self.kwargs['pet_id']
        serializer.save(pet_id=pet_id)