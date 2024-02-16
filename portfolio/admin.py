from django.contrib import admin
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.models import FlatPage
from django.db import models
from django.utils.translation import gettext as _
from leaflet.admin import LeafletGeoAdminMixin
from modeltranslation.admin import TranslationAdmin, TranslationTabularInline
from tinymce.widgets import TinyMCE

from .models import Activity, Client, Intervention, Project, ProjectCarousel, ProjectMap


class TinyMCEFlatPageAdmin(FlatPageAdmin):
    fieldsets = (
        (None, {"fields": ("url", "title", "content", "sites")}),
        (
            _("Advanced options"),
            {
                "fields": (
                    # 'enable_comments',
                    "registration_required",
                    "template_name",
                ),
            },
        ),
    )

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == "content":
            return db_field.formfield(
                widget=TinyMCE(
                    attrs={"cols": 80, "rows": 30},
                )
            )
        return super().formfield_for_dbfield(db_field, **kwargs)


# Re-register FlatPageAdmin
admin.site.unregister(FlatPage)
admin.site.register(FlatPage, TinyMCEFlatPageAdmin)


class ProjectCarouselInline(TranslationTabularInline):
    model = ProjectCarousel
    fields = (
        "position",
        "fb_image",
        "description",
    )
    extra = 0


class ProjectMapInline(LeafletGeoAdminMixin, admin.TabularInline):
    model = ProjectMap
    fields = ("geom",)
    extra = 0


@admin.register(Project)
class ProjectAdmin(TranslationAdmin):
    list_display = (
        "title",
        "intro",
    )
    inlines = [
        ProjectMapInline,
        ProjectCarouselInline,
    ]
    formfield_overrides = {
        models.TextField: {"widget": TinyMCE},
    }

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "title",
                    "intro",
                    "date",
                    "date_end",
                    "client",
                ),
            },
        ),
        (
            _("Text"),
            {
                "fields": ("body",),
            },
        ),
        (
            _("Meta"),
            {
                "fields": (
                    "site",
                    "type",
                    "status",
                    "cost",
                    "activity",
                ),
            },
        ),
    )


@admin.register(Activity)
class ActivityAdmin(TranslationAdmin):
    list_display = (
        "full",
        "position",
    )
    list_editable = ("position",)


@admin.register(Intervention)
class InterventionAdmin(TranslationAdmin):
    list_display = (
        "name",
        "position",
    )
    list_editable = ("position",)


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("name",)
