from django import forms
from django.core.validators import RegexValidator
from catalog.models import Pet, Breed
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


class PersonCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields


active_need = RegexValidator(
    regex=r"^(10|[1-9])$",
    message="Digit in range 1 to 10",
)


class BreedCreationForm(forms.ModelForm):
    active_need = forms.IntegerField(
        validators=[active_need],
    )
    active_need = forms.IntegerField(required=False,)
    description = forms.CharField(required=False, widget=forms.Textarea)
    class Meta:
        model = Breed
        fields = ("name",
                  "type",
                  "active_need",
                  "description")


class PetForm(forms.ModelForm):
    class Meta:
        model = Pet
        exclude = ["visitors"]