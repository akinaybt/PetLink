from django.urls import path
from .views import PetCreateView, MedicationView, FeedingView, WalkView


urlpatterns = [
    path('pet-create/', PetCreateView.as_view(), name='pet-create'),
    path('medications/', MedicationView.as_view(), name='medications'),
    path('feedings/', FeedingView.as_view(), name='feedings'),
    path('walks/', WalkView.as_view(), name='walks'),

]


