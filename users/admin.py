from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.models import FlatPage
from django.utils.translation import gettext as _
from modeltranslation.admin import TranslationTabularInline
from tinymce.widgets import TinyMCE

from .models import Profile, User, UserMessage


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


class ProfileAdmin(TranslationTabularInline):
    model = Profile
    # exclude = ("temp_image",)
    extra = 0


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ("username", "is_staff", "is_active", "is_superuser")
    list_editable = ("is_staff", "is_active")
    inlines = [
        ProfileAdmin,
    ]


@admin.register(UserMessage)
class UserMessageAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "subject",
    )
