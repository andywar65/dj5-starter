from django.contrib import admin

from .models import Shotgun, ShotgunImage


class ShotgunImageInline(admin.TabularInline):
    model = ShotgunImage
    fields = (
        "position",
        "description",
        "filer_image",
    )
    extra = 0


@admin.register(Shotgun)
class ShotgunAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "date",
    )
    exclude = ("image",)
    inlines = [
        ShotgunImageInline,
    ]
