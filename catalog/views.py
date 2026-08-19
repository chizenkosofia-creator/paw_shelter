from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import UserPassesTestMixin
from catalog.forms import PetForm, BreedCreationForm, PersonCreationForm
from catalog.models import Pet, Breed
from django.urls import reverse_lazy
from django.views import generic


User = get_user_model()


def index(request):
    num_pets = Pet.objects.count()
    num_adopted = Pet.objects.filter(status=Pet.Status.adoption).count()
    featured_pets = Pet.objects.filter(status=Pet.Status.under_treatment)[:3]
    total_pets = Pet.objects.count()
    pets_ready_for_adoption = Pet.objects.filter(status=Pet.Status.ready_for_adoption).count()

    context = {
        "num_pets": num_pets,
        "num_adopted": num_adopted,
        "featured_pets": featured_pets,
        "total_pets": total_pets,
        "pets_ready_for_adoption": pets_ready_for_adoption,
    }

    return render(request, "catalog/index.html", context=context)


class RegisterView(generic.CreateView):
    form_class = PersonCreationForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("login")


class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_staff


class PersonListView(LoginRequiredMixin, generic.DeleteView):
    model = User


class PersonDetailView(LoginRequiredMixin, generic.DetailView):
    model = User
    queryset = User.objects.all()


class PersonDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = User
    template_name = "catalog/person_confirm_delete.html"
    success_url = reverse_lazy("catalog:person-list")


class PersonUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = User
    fields = ["first_name", "last_name", "email"]
    template_name = "catalog:person-list"

    def get_success_url(self):
        return reverse_lazy("catalog:person-detail",
                            kwargs={"pk": self.object.pk})


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


@login_required
def toggle_favorite_pet(request, pk):
    pet = get_object_or_404(Pet, id=pk)
    if request.user in pet.visitors.all():
        pet.visitors.remove(request.user)
    else:
        pet.visitors.add(request.user)
    return HttpResponseRedirect(reverse_lazy(
        "catalog:pet-detail", args=[pk]))


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
