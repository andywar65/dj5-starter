from django.shortcuts import get_object_or_404
from django.utils.crypto import get_random_string
from django.utils.translation import gettext as _
from django.views.generic import DetailView, ListView

from .choices import CATEGORY, STATUS
from .models import Intervention, Project, ProjectCarousel, ProjectMap


class HxPageTemplateMixin:
    def get_template_names(self):
        if not self.request.htmx:
            return [self.template_name.replace("htmx/", "")]
        elif "page" in self.request.GET:
            return ["portfolio/includes/infinite_scroll.html"]
        else:
            return [self.template_name]


class ProjectListView(HxPageTemplateMixin, ListView):
    model = Project
    context_object_name = "progs"
    paginate_by = 6
    template_name = "portfolio/htmx/project_list.html"

    def get_queryset(self):
        prog_list = (
            ProjectCarousel.objects.all().values_list("home", flat=True).distinct()
        )
        qs = Project.objects.filter(id__in=prog_list).prefetch_related(
            "client", "type", "activity"
        )
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["all_projects"] = False
        return context


class ProjectListMapView(HxPageTemplateMixin, ListView):
    model = ProjectMap
    template_name = "portfolio/htmx/project_map.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["all_projects"] = True
        context["layer_list"] = [_("Selected"), _("Others")]
        return context


class ProjectListAllView(ProjectListView):
    def get_queryset(self):
        qs = Project.objects.all().prefetch_related("client", "type", "activity")
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["all_projects"] = True
        return context


class ProjectYearArchiveView(ProjectListView):
    template_name = "portfolio/htmx/project_archive_year.html"

    def get_queryset(self):
        year = self.kwargs["year"]
        qs = Project.objects.filter(date__year=year)
        qs2 = (
            Project.objects.exclude(date_end=None)
            .filter(date__year__lt=year)
            .exclude(date_end__year__lt=year)
        )
        qs = qs | qs2
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["year"] = self.kwargs["year"]
        context["next_year"] = context["year"] + 1
        context["previous_year"] = context["year"] - 1
        return context


class ProjectCategoryListView(HxPageTemplateMixin, ListView):
    model = Project
    context_object_name = "progs"
    template_name = "portfolio/htmx/project_category_list.html"
    paginate_by = 6
    allow_empty = False

    def get_readable(self, list, target):
        for i in list:
            if i[0] == target:
                return i[1]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if "category" in self.request.GET:
            readable = self.get_readable(CATEGORY, self.request.GET["category"])
            context["cat_filter"] = _("in Category: %(read)s") % {"read": readable}
        elif "type" in self.request.GET:
            readable = get_object_or_404(Intervention, id=self.request.GET["type"]).name
            context["cat_filter"] = _("with Intervention type: %(read)s") % {
                "read": readable
            }
        elif "status" in self.request.GET:
            readable = self.get_readable(STATUS, self.request.GET["status"])
            context["cat_filter"] = _("with Status: %(read)s") % {"read": readable}
        elif "cost" in self.request.GET:
            readable = self.request.GET["cost"]
            context["cat_filter"] = _("with Cost € %(read)s or lower") % {
                "read": readable
            }
        return context

    def get_queryset(self):
        qs = super().get_queryset()
        if "category" in self.request.GET:
            qs = qs.filter(category=self.request.GET["category"])
        elif "type" in self.request.GET:
            qs = qs.filter(type=self.request.GET["type"])
        elif "status" in self.request.GET:
            qs = qs.filter(status=self.request.GET["status"])
        elif "cost" in self.request.GET:
            cost = self.request.GET["cost"].replace(",", ".")
            qs = qs.filter(cost__lte=float(cost)).order_by("-cost")
        return qs


class ProjectDetailView(DetailView):
    model = Project
    context_object_name = "prog"
    slug_field = "slug"
    template_name = "portfolio/htmx/project_detail.html"

    def get_template_names(self):
        if not self.request.htmx:
            return [self.template_name.replace("htmx/", "")]
        else:
            return [self.template_name]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # we add the following to feed standardized gallery
        context["main_gal_slug"] = get_random_string(7)
        context["title"] = self.object.title
        # gallery images
        context["images"] = self.object.project_carousel.all()
        return context
