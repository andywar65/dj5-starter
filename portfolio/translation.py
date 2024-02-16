from modeltranslation.translator import TranslationOptions, register

from .models import Activity, Client, Intervention, Project, ProjectCarousel


@register(Project)
class ProjectTranslationOptions(TranslationOptions):
    fields = (
        "slug",
        "title",
        "intro",
        "body",
        "site",
    )


@register(ProjectCarousel)
class ProjectCarouselTranslationOptions(TranslationOptions):
    fields = ("description",)


@register(Activity)
class ActivityTranslationOptions(TranslationOptions):
    fields = ("full",)


@register(Intervention)
class InterventionTranslationOptions(TranslationOptions):
    fields = ("name",)


@register(Client)
class ClientTranslationOptions(TranslationOptions):
    fields = ("name",)
