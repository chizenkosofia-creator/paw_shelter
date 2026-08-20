from django.test import TestCase
from catalog.forms import PersonCreationForm, BreedCreationForm, PetForm
from catalog.models import Breed, Pet


class FormsTests(TestCase):
    def test_person_creation_form_valid_data(self) -> None:
        form_data = {
            "username": "testuser",
            "password1": "StrongPass123!",
            "password2": "StrongPass123!",
        }
        form = PersonCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_person_creation_form_passwords_mismatch(self) -> None:
        form_data = {
            "username": "testuser",
            "password1": "StrongPass123!",
            "password2": "DifferentPass123!",
        }
        form = PersonCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("password2", form.errors)

    def test_breed_creation_form_valid_data(self) -> None:
        form_data = {
            "name": "Golden Retriever",
            "type": "Dog",
            "active_need": 8,
            "description": "Friendly and energetic.",
        }
        form = BreedCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["active_need"], 8)

    def test_breed_creation_form_optional_fields_empty(self) -> None:
        form_data = {
            "name": "Persian",
            "type": "Cat",
            "active_need": "",
            "description": "",
        }
        form = BreedCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_breed_creation_form_active_need_out_of_range(self) -> None:
        form_data = {
            "name": "Dogy",
            "type": "Dog",
            "active_need": 15,
            "description": "",
        }
        form = BreedCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("active_need", form.errors)

    def test_pet_form_valid_data(self) -> None:
        breed = Breed.objects.create(name="Labrador", type="Dog")
        form_data = {
            "name": "Gubby",
            "age": 3,
            "breed": breed.id,
        }
        form = PetForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_pet_form_excludes_visitors_field(self) -> None:
        form = PetForm()
        self.assertNotIn("visitors", form.fields)
