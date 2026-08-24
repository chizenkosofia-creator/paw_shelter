from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Person, Pet, Breed


@admin.register(Person)
class PersonAdmin(UserAdmin):
    list_display = UserAdmin.list_display
    fieldsets = UserAdmin.fieldsets
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            (
                "Additional info",
                {
                    "fields": (
                        "first_name",
                        "last_name",
                    )
                },
            ),
        )
    )


@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    search_fields = ("model",)
    list_filter = ("breed",)


admin.site.register(Breed)
