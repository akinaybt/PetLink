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
    GenericAPIView для просмотра и создания питомцев.
    - Обычные пользователи видят только своих питомцев.
    - Администраторы видят всех питомцев.
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
    serializer_class = MedicationSerializer

    def get_queryset(self):
        return Medication.objects.filter(pet__owner=self.request.user)

    def perform_create(self, serializer):
        medication = serializer.save()

class FeedingView(ListCreateAPIView):
    serializer_class = FeedingSerializer

    def get_queryset(self):
        return Feeding.objects.filter(pet__owner=self.request.user)

    def perform_create(self, serializer):
        activity = serializer.save()

class WalkView(ListCreateAPIView):
    serializer_class = WalkSerializer

    def get_queryset(self):
        return Walk.objects.filter(pet__owner=self.request.user)

    def perform_create(self, serializer):
        walk = serializer.save()

class AppointmentView(ListCreateAPIView):
    serializer_class = AppointmentSerializer

    def get_queryset(self):
        return Appointment.objects.filter(pet__owner=self.request.user)


class PetDocumentView(ListCreateAPIView):
    """
    API для загрузки и получения документов питомца.
    """
    serializer_class = PetDocumentSerializer

    def get_queryset(self):
        """
        Получить список документов для конкретного питомца.
        """
        pet_id = self.kwargs['pet_id']
        return PetDocument.objects.filter(pet_id=pet_id)

    def perform_create(self, serializer):
        """
        Устанавливаем связь документа с питомцем во в��емя создания.
        """
        pet_id = self.kwargs['pet_id']
        serializer.save(pet_id=pet_id)