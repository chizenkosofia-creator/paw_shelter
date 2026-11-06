from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import UserPassesTestMixin
from catalog.forms import PetForm, BreedCreationForm, PersonCreationForm
from catalog.models import Pet, Breed, Person
from django.urls import reverse_lazy, reverse
from django.views import generic, View

User = get_user_model()


class IndexView(generic.TemplateView):
    template_name = "catalog/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["num_pets"] = Pet.objects.count()
        context["num_adopted"] = Pet.objects.filter(status=Pet.Status.adoption).count()
        context["featured_pets"] = Pet.objects.filter(status=Pet.Status.under_treatment)[:3]
        context["total_pets"] = Pet.objects.count()
        context["pets_ready_for_adoption"] = Pet.objects.filter(
            status=Pet.Status.ready_for_adoption
        ).count()
        return context

class RegisterView(generic.CreateView):
    form_class = PersonCreationForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("login")


class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_staff


class PersonCreateView(generic.CreateView):
    model = Person
    form_class = PersonCreationForm
    template_name = "catalog/person_form.html"
    success_url = reverse_lazy("catalog:person-detail")


class PersonListView(LoginRequiredMixin, generic.ListView):
    model = User


class PersonDetailView(LoginRequiredMixin, generic.DetailView):
    model = User
    queryset = User.objects.all()


class PersonDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = User
    template_name = "catalog/person_confirm_delete.html"
    success_url = reverse_lazy("catalog:person-detail")


class PersonUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = User
    fields = ["first_name", "last_name", "email"]
    template_name = "catalog/person_form.html"

    def get_success_url(self):
        return reverse("catalog:person-detail", kwargs={"pk": self.object.pk})


class PetListView(generic.ListView):
    model = Pet
    template_name = "catalog/pet_list.html"
    paginate_by = 5

    def get_queryset(self):
        queryset = Pet.objects.select_related("breed")
        name = self.request.GET.get("name")
        if name:
            queryset = queryset.filter(
                Q(name__icontains=name) | Q(breed__name__icontains=name)
            )
        species = self.request.GET.get("type")
        if species:
            queryset = queryset.filter(breed__type__iexact=species)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_name"] = self.request.GET.get("name", "")
        context["search_type"] = self.request.GET.get("type", "")
        return context


class PetDetailView(generic.DetailView):
    model = Pet
    template_name = "catalog/pet_detail.html"


class PetCreateView(AdminRequiredMixin, generic.CreateView):
    model = Pet
    form_class = PetForm
    success_url = reverse_lazy("catalog:pet-list")


class PetUpdateView(AdminRequiredMixin, generic.UpdateView):
    model = Pet
    form_class = PetForm
    success_url = reverse_lazy("catalog:pet-list")


class PetDeleteView(AdminRequiredMixin, generic.DeleteView):
    model = Pet
    template_name = "catalog/pet_confirm_delete.html"
    success_url = reverse_lazy("catalog:pet-list")


class ToggleFavoritePetView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        pet = get_object_or_404(Pet, id=pk)
        if request.user in pet.visitors.all():
            pet.visitors.remove(request.user)
        else:
            pet.visitors.add(request.user)
        return HttpResponseRedirect(reverse("catalog:pet-detail", args=[pk]))

class BreedListView(generic.ListView):
    model = Breed
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.GET.get("name")
        if name:
            queryset = queryset.filter(
                Q(name__icontains=name) | Q(type__icontains=name)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_name"] = self.request.GET.get("name", "")
        return context


class BreedDetailView(generic.DetailView):
    model = Breed
    template_name = "catalog/breed_detail.html"
    context_object_name = "breed"


class BreedCreateView(AdminRequiredMixin, generic.CreateView):
    model = Breed
    form_class = BreedCreationForm
    success_url = reverse_lazy("catalog:breed-list")


class BreedUpdateView(AdminRequiredMixin, generic.UpdateView):
    model = Breed
    form_class = BreedCreationForm
    success_url = reverse_lazy("catalog:breed-list")


class BreedDeleteView(AdminRequiredMixin, generic.DeleteView):
    model = Breed
    template_name = "catalog/breed_confirm_delete.html"
    success_url = reverse_lazy("catalog:breed-list")


class HowToHelpView(generic.TemplateView):
    template_name = "catalog/how_to_help.html"
