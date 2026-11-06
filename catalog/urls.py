from django.urls import path
from django.views import View

from .views import (
    IndexView,
    PetListView,
    PetDetailView,
    PetCreateView,
    PetUpdateView,
    PetDeleteView,
    PersonCreateView,
    PersonListView,
    PersonDetailView,
    PersonDeleteView,
    PersonUpdateView,
    BreedListView,
    BreedCreateView,
    BreedDetailView,
    BreedUpdateView,
    BreedDeleteView,
    ToggleFavoritePetView,
    RegisterView,
    HowToHelpView,
)
app_name = "catalog"
urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("register/", RegisterView.as_view(), name="register"),
    path("breeds/<int:pk>/", BreedDetailView.as_view(), name="breed-detail"),
    path("breeds/", BreedListView.as_view(), name="breed-list"),
    path("breeds/create/", BreedCreateView.as_view(), name="breed-create"),
    path("breeds/<int:pk>/update/", BreedUpdateView.as_view(), name="breed-update"),
    path("breeds/<int:pk>/delete/", BreedDeleteView.as_view(), name="breed-delete"),

    path("pets/", PetListView.as_view(), name="pet-list"),
    path("pets/<int:pk>/", PetDetailView.as_view(), name="pet-detail"),
    path("pets/create/", PetCreateView.as_view(), name="pet-create"),
    path("pets/<int:pk>/update/", PetUpdateView.as_view(), name="pet-update"),
    path("pets/<int:pk>/delete/", PetDeleteView.as_view(), name="pet-delete"),
    path("people/create/", PersonCreateView.as_view(), name="person-create"),
    path("people/", PersonListView.as_view(), name="person-list"),
    path("people/<int:pk>/", PersonDetailView.as_view(), name="person-detail"),
    path("people/<int:pk>/delete/", PersonDeleteView.as_view(), name="person-delete"),
    path("people/<int:pk>/update/", PersonUpdateView.as_view(), name="person-update"),
    path("people/<int:pk>/toggle-assign/", ToggleFavoritePetView.as_view(), name="assign_to_pet"),

    path("how-to-help/", HowToHelpView.as_view(), name="how-to-help"),
]
