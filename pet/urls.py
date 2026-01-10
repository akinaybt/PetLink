from django.urls import path
from .views import PetCreateView, MedicationView, FeedingView, WalkView, AppointmentView, PetDocumentView

urlpatterns = [
    path('pet-create/', PetCreateView.as_view(), name='pet-create'),
    path('medications/', MedicationView.as_view(), name='medications'),
    path('feedings/', FeedingView.as_view(), name='feedings'),
    path('walks/', WalkView.as_view(), name='walks'),
    path('appointments/', AppointmentView.as_view(), name='appointments'),
    path('pets/<int:pet_id>/documents/', PetDocumentView.as_view(), name='pet-documents'),

]


