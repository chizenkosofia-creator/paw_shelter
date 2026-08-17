from django.contrib import admin

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Person, Pet, Breed


@admin.register(Person)
class PersonAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("about_user",)
    fieldsets = UserAdmin.fieldsets + (
        (("Additional info", {"fields": ("about_user",)}),)
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            (
                "Additional info",
                {
                    "fields": (
                        "first_name",
                        "last_name",
                        "about_user",
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
