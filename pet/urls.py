from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'pets', views.PetViewSet, basename='pet')
router.register(r'vaccinations', views.VaccinationRecordViewSet, basename='vaccination')
router.register(r'appointments', views.VeterinaryAppointmentViewSet, basename='appointment')
router.register(r'care-logs', views.DailyCareLogViewSet, basename='care-log')
router.register(r'reminders', views.ReminderViewSet, basename='reminder')
router.register(r'documents', views.PetDocumentViewSet, basename='document')

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]