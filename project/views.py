from django import forms
from django.contrib.flatpages.models import FlatPage
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.core.exceptions import ImproperlyConfigured
from django.http import Http404
from django.template.response import TemplateResponse
from django.urls import reverse
from neapolitan.views import CRUDView


def check_htmx_request(request):
    """Helper function"""

    if not request.htmx:
        raise Http404("Request without HTMX headers")


def home(request):
    template_name = "htmx/home.html"
    if not request.htmx:
        template_name = template_name.replace("htmx/", "")
    context = {}
    return TemplateResponse(request, template_name, context)


def nav_bar(request):
    check_htmx_request(request)
    template_name = "navbar.html"
    context = {"user": request.user}
    return TemplateResponse(request, template_name, context)


def search_box(request):
    check_htmx_request(request)
    template_name = "htmx/searchbox.html"
    return TemplateResponse(request, template_name, {})


class ValidateForm(forms.Form):
    q = forms.CharField(max_length=100)


def search_results(request):
    success = False
    template_name = "htmx/search_results.html"
    if not request.htmx:
        template_name = template_name.replace("htmx/", "")
    form = ValidateForm(request.GET)
    if form.is_valid():
        q = SearchQuery(request.GET["q"])
        v = SearchVector("url", "title", "content", "sites")
        # search in flatpages
        l_code = f"/{request.LANGUAGE_CODE}/"
        flatpages = FlatPage.objects.filter(url__startswith=l_code).annotate(
            rank=SearchRank(v, q)
        )
        flatpages = flatpages.filter(rank__gt=0.01)
        if flatpages:
            flatpages = flatpages.order_by("-rank")
            success = True

        return TemplateResponse(
            request,
            template_name,
            {
                "search": request.GET["q"],
                "flatpages": flatpages,
                "success": success,
            },
        )
    else:
        return TemplateResponse(
            request,
            template_name,
            {
                "success": success,
            },
        )


class HxCRUDView(CRUDView):

    def get_context_data(self, **kwargs):
        kwargs["view"] = self
        kwargs["object_verbose_name"] = self.model._meta.verbose_name
        kwargs["object_verbose_name_plural"] = self.model._meta.verbose_name_plural
        kwargs["create_view_url"] = reverse(f"{self.url_base}-create")
        # add list view url
        kwargs["list_view_url"] = reverse(f"{self.url_base}-list")

        if getattr(self, "object", None) is not None:
            kwargs["object"] = self.object
            # add detail view url
            kwargs["detail_view_url"] = reverse(
                f"{self.url_base}-detail", kwargs={"pk": self.object.id}
            )
            context_object_name = self.get_context_object_name()
            if context_object_name:
                kwargs[context_object_name] = self.object

        if getattr(self, "object_list", None) is not None:
            kwargs["object_list"] = self.object_list
            context_object_name = self.get_context_object_name(is_list=True)
            if context_object_name:
                kwargs[context_object_name] = self.object_list

        return kwargs

    def get_template_names(self):
        """
        Returns a list of template names to use when rendering the response.

        If `.template_name` is not specified, uses the
        "{app_label}/{model_name}{template_name_suffix}.html" model template
        pattern, with the fallback to the
        "neapolitan/object{template_name_suffix}.html" default templates.
        """
        if self.template_name is not None:
            return [self.template_name]

        if self.model is not None and self.template_name_suffix is not None:
            # check if request has a HTMX header, pick partial template
            if self.request.htmx:
                return [
                    f"{self.model._meta.app_label}/"
                    f"{self.model._meta.object_name.lower()}"
                    f"{self.template_name_suffix}.html",
                    f"neapolitan/htmx/object{self.template_name_suffix}.html",
                ]
            return [
                f"{self.model._meta.app_label}/"
                f"{self.model._meta.object_name.lower()}"
                f"{self.template_name_suffix}.html",
                f"neapolitan/object{self.template_name_suffix}.html",
            ]
        msg = (
            "'%s' must either define 'template_name' or 'model' and "
            "'template_name_suffix', or override 'get_template_names()'"
        )
        raise ImproperlyConfigured(msg % self.__class__.__name__)
