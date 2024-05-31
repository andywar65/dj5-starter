from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse
from django.utils.text import slugify
from django.views.generic import DetailView
from django.views.generic.dates import ArchiveIndexView
from django.views.generic.edit import FormView
from filer.models import Image

from .forms import ShotgunCreateForm
from .models import Shotgun, ShotgunImage


class HxPageTemplateMixin:
    """Switches template depending on request.htmx and pagination"""

    def get_template_names(self):
        if not self.request.htmx:
            return [self.template_name.replace("htmx/", "")]
        elif "page" in self.request.GET:
            return ["pages/includes/infinite_scroll.html"]
        else:
            return [self.template_name]


class ShotgunArchiveIndexView(ArchiveIndexView):
    model = Shotgun
    date_field = "date"
    context_object_name = "shots"
    paginate_by = 6
    allow_empty = True
    template_name = "pages/htmx/shotgun_index.html"

    def get_template_names(self):
        if not self.request.htmx:
            return [self.template_name.replace("htmx/", "")]
        elif "page" in self.request.GET:
            return ["pages/includes/infinite_shotgun.html"]
        else:
            return [self.template_name]


class ShotgunDetailView(DetailView):
    model = Shotgun
    context_object_name = "shot"
    template_name = "pages/htmx/shotgun_detail.html"

    def get_template_names(self):
        if not self.request.htmx:
            return [self.template_name.replace("htmx/", "")]
        else:
            return [self.template_name]


class ShotgunCreateFormView(PermissionRequiredMixin, FormView):
    form_class = ShotgunCreateForm
    template_name = "pages/htmx/shotgun_create.html"
    permission_required = "pages.add_shotgun"

    def get_template_names(self):
        if not self.request.htmx:
            return [self.template_name.replace("htmx/", "")]
        else:
            return [self.template_name]

    def form_valid(self, form):
        # assign Shotgun form fields
        user = self.request.user
        title = form.cleaned_data["title"]
        body = form.cleaned_data["body"]
        # create shotgun
        shot = Shotgun.objects.create(title=title, body=body)
        # create filer image
        image = Image.objects.create(
            owner=user,
            original_filename=slugify(title),
            file=form.cleaned_data["image"],
        )
        # create ShotgunImage
        description = form.cleaned_data["description"]
        img = ShotgunImage(shot_id=shot.id, filer_image=image, description=description)
        img.save()

        return super(ShotgunCreateFormView, self).form_valid(form)

    def get_success_url(self):
        return reverse("shotgun_index")
