from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import *
from .serializers import *
# from .permissions import IsOwner

# Create your views here.

class PetViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows pets to be viewed or edited.
    - Users can only see and manage their own pets.
    - Admins can see and manage all pets.
    """
    serializer_class = PetSerializer
    # permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        """
        This view should return a list of all the pets
        for the currently authenticated user.
        """
        if self.request.user.is_staff:
            return Pet.objects.all() # Admin users see all pets
        return Pet.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        """
        Assign the current user as the owner of the new pet.
        """
        serializer.save(owner=self.request.user)


class ReminderViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows reminders to be viewed or edited.
    - Users can only manage reminders for pets they own.
    """
    serializer_class = ReminderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        This view should return a list of all reminders for the pets
        owned by the currently authenticated user.
        """
        if self.request.user.is_staff:
            return Reminder.objects.all() # Admin users see all reminders
        return Reminder.objects.filter(pet__owner=self.request.user)

    def get_serializer_context(self):
        """
        Pass the request context to the serializer.
        """
        return {'request': self.request}

class PetDocumentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows pet documents to be viewed or edited.
    """
    serializer_class = PetDocumentSerializer

    def get_queryset(self):
        """
        This view should return a list of all documents for
        the pets owned by the currently authenticated user.
        """
        return PetDocument.objects.filter(pet__owner=self.request.user)
