from django.conf import settings
from django.contrib.sites.models import Site
from django.db import models
from django.urls import reverse
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from djgeojson.fields import PointField
from easy_thumbnails.files import get_thumbnailer
from filer.fields.image import FilerImageField

from project.utils import generate_unique_slug  # check_wide_image

from .choices import CATEGORY, STATUS


def project_default_intro():
    # following try/except for test to work
    try:
        current_site = Site.objects.get_current()
        return _("Another project by %(name)s!") % {"name": current_site.name}
    except Site.DoesNotExist:
        return _("Another project by this site!")


class Activity(models.Model):
    full = models.CharField(
        max_length=50,
        verbose_name=_("Name"),
    )
    position = models.PositiveSmallIntegerField(_("Position"), null=True)

    def __str__(self):
        return self.full

    class Meta:
        verbose_name = _("Activity")
        verbose_name_plural = _("Activities")
        ordering = ("position",)


class Intervention(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name=_("Name"),
    )
    position = models.PositiveSmallIntegerField(_("Position"), null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Intervention")
        verbose_name_plural = _("Interventions")
        ordering = ("position",)


class Client(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name=_("Name"),
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Client")
        verbose_name_plural = _("Clients")


class Project(models.Model):
    slug = models.SlugField(
        _("Slug"),
        max_length=100,
        null=True,
        blank=True,
        help_text=_(
            """Appears on the address bar.
            Automatically generated for the active language
            """
        ),
    )
    title = models.CharField(
        _("Title"),
        help_text=_("Title of the project"),
        max_length=50,
        null=True,
    )
    intro = models.CharField(_("Introduction"), null=True, blank=True, max_length=100)
    body = models.TextField(_("Text"), null=True, blank=True)
    date = models.DateField(
        _("Start date"),
        default=now,
    )
    date_end = models.DateField(
        _("End date"),
        null=True,
        blank=True,
    )
    site = models.CharField(
        _("Site"),
        null=True,
        blank=True,
        help_text=_("Loose location"),
        max_length=100,
    )
    client = models.ManyToManyField(
        Client,
        blank=True,
        verbose_name=_("Client"),
    )
    category = models.CharField(
        max_length=4,
        choices=CATEGORY,
        default="ALT",
        verbose_name=_("Functional category"),
    )
    type = models.ManyToManyField(
        Intervention,
        blank=True,
        verbose_name=_("Type of intervention"),
    )
    status = models.CharField(
        max_length=4,
        choices=STATUS,
        default="ALT",
        verbose_name=_("Status of intervention"),
    )
    cost = models.DecimalField(
        max_digits=11,
        decimal_places=2,
        default=0.00,
        verbose_name=_("Cost of intervention"),
    )
    activity = models.ManyToManyField(
        Activity,
        blank=True,
        verbose_name=_("Performed activities"),
    )

    class Meta:
        verbose_name = _("Project")
        verbose_name_plural = _("Projects")
        ordering = ("-date",)

    def __str__(self):
        return self.title

    def get_full_path(self):
        return reverse("portfolio:project_detail", kwargs={"slug": self.slug})

    def get_activities(self):
        list = []
        for act in self.activity.all():
            list.append(act.full)
        s = ", "
        s = s.join(list)
        return s

    def get_clients(self):
        list = []
        for cln in self.client.all():
            list.append(cln.name)
        s = ", "
        s = s.join(list)
        return s

    def save(self, *args, **kwargs):
        if self.title_it and not self.slug_it:
            self.slug_it = generate_unique_slug(Project, self.title_it)
        if self.title_de and not self.slug_de:
            self.slug_de = generate_unique_slug(Project, self.title_de)
        super(Project, self).save(*args, **kwargs)
        p, created = ProjectMap.objects.get_or_create(prog_id=self.id)


class ProjectMap(models.Model):
    prog = models.OneToOneField(
        Project, on_delete=models.CASCADE, primary_key=True, editable=False
    )
    geom = PointField(_("Location"), null=True)

    class Meta:
        verbose_name = _("Map")
        verbose_name_plural = _("Maps")

    @property
    def popupContent(self):
        url = reverse(
            "portfolio:project_detail",
            kwargs={"slug": self.prog.slug},
        )
        title_str = '<h5><a href="%(url)s">%(title)s</a></h5>' % {
            "title": self.prog.title,
            "url": url,
        }
        intro_str = "<small>%(intro)s</small>" % {"intro": self.prog.intro}
        image = self.prog.project_carousel.first()
        if not image:
            return {
                "content": title_str + intro_str,
                "layer": _("Others"),
            }
        thumbnailer = get_thumbnailer(image.fb_image)
        thumb = thumbnailer.get_thumbnail({"size": (256, 256), "crop": True})
        image_str = '<img src="%(image)s">' % {"image": thumb.url}
        return {
            "content": title_str + image_str + intro_str,
            "layer": _("Selected"),
        }

    def get_thumbnail_path(self):
        image = self.prog.project_carousel.first()
        if not image:
            return
        path = image.fb_image.version_generate("popup").path
        return settings.MEDIA_URL + path


class ProjectCarousel(models.Model):
    home = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="project_carousel",
        verbose_name=_("Project"),
    )
    fb_image = FilerImageField(related_name="carousel_image", on_delete=models.CASCADE)
    description = models.CharField(
        _("Description"),
        help_text=_("Will be used in captions"),
        max_length=100,
        null=True,
        blank=True,
    )
    position = models.PositiveSmallIntegerField(_("Position"), null=True)

    class Meta:
        verbose_name = _("Project carousel")
        verbose_name_plural = _("Project carousels")
        ordering = [
            "position",
        ]

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # check_wide_image(self.fb_image)
