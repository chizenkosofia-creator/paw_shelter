from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse


class Breed(models.Model):
    name = models.CharField(max_length=255, unique=True)
    type = models.CharField(max_length=255)
    active_need = models.IntegerField(
        help_text="Activity level from 1 to 10")
    description = models.TextField()

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.type} ({self.name})"


class Person(AbstractUser):
    about_user = models.TextField()

    class Meta:
        verbose_name = "person"
        verbose_name_plural = "people"

    def __str__(self):
        return f"{self.username} ({self.first_name} {self.last_name})"

    def get_absolute_url(self):
        return reverse("catalog:person-detail", kwargs={"pk": self.pk})



class Pet(models.Model):
    gender_choise = [
        ("M", "Male"),
        ("F", "Female"),
    ]
    name = models.CharField(max_length=255)
    breed = models.ForeignKey(Breed, on_delete=models.CASCADE, related_name="pets")
    image = models.ImageField(upload_to="pets/", blank=True, null=True)
    gender = models.CharField(max_length=1, choices=gender_choise, default="F")
    age_months = models.PositiveIntegerField(default=12)
    story = models.TextField(blank=True, help_text="Rescue story and character description")
    visitors = models.ManyToManyField(Person, related_name="pets", blank=True)


    class Status(models.TextChoices):
        under_treatment = "UT", "Under Treatment / In Shelter"
        ready_for_adoption = "RA", "Ready for Adoption"
        adoption = "AD", "Adopted"

    status = models.CharField(
        max_length=2,
        choices=Status.choices,
        default=Status.under_treatment,
        help_text="Current status of the pet"
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("catalog:pet-detail", kwargs={"pk": self.pk})

    @property
    def age_display(self):
        years = self.age_months // 12
        months = self.age_months % 12
        if years > 0:
            return f"{years} y.o." if months == 0 else f"{years}y {months}m"
        return f"{months} months"
