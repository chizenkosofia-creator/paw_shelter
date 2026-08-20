from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from catalog.models import Pet, Breed

User = get_user_model()


class ViewsTests(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username="testuser",
            password="Password123!"
        )
        self.admin_user = User.objects.create_superuser(
            username="adminuser",
            password="Password123!"
        )
        self.breed = Breed.objects.create(name="Golden Retriever", type="Dog")
        self.pet = Pet.objects.create(name="Buddy", age=3, breed=self.breed)

    def test_index_view_context(self) -> None:
        response = self.client.get(reverse("catalog:index"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("num_pets", response.context)
        self.assertEqual(response.context["num_pets"], 1)

    def test_person_list_view_login_required(self) -> None:
        url = reverse("catalog:person-list")
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(response, f"/accounts/login/?next={url}")

    def test_person_list_view_authenticated(self) -> None:
        self.client.force_login(self.user)
        response = self.client.get(reverse("catalog:person-list"))
        self.assertEqual(response.status_code, 200)

    def test_pet_list_view_search_filter(self) -> None:
        Pet.objects.create(
            name="Whiskers",
            age=2,
            breed=Breed.objects.create(name="Persian", type="Cat")
        )
        response = self.client.get(reverse("catalog:pet-list"), {"name": "Buddy"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["pet_list"]), 1)
        self.assertEqual(response.context["pet_list"][0].name, "Buddy")

    def test_pet_create_view_forbidden_for_regular_user(self) -> None:
        self.client.force_login(self.user)
        response = self.client.get(reverse("catalog:pet-create"))
        self.assertEqual(response.status_code, 430)

    def test_pet_create_view_allowed_for_admin(self) -> None:
        self.client.force_login(self.admin_user)
        response = self.client.get(reverse("catalog:pet-create"))
        self.assertEqual(response.status_code, 200)

    def test_toggle_favorite_pet_view(self) -> None:
        self.client.force_login(self.user)
        url = reverse("catalog:toggle-favorite-pet", kwargs={"pk": self.pet.pk})
        response = self.client.get(url)
        self.assertRedirects(response, reverse("catalog:pet-detail", args=[self.pet.pk]))
        self.assertTrue(self.pet.visitors.filter(id=self.user.id).exists())
        self.client.get(url)
        self.assertFalse(self.pet.visitors.filter(id=self.user.id).exists())
