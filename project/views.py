from django import forms
from django.contrib.flatpages.models import FlatPage
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.http import Http404
from django.template.response import TemplateResponse


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
        if request.GET["lang"] == "it":
            flatpages = FlatPage.objects.filter(url__startswith="/documenti/").annotate(
                rank=SearchRank(v, q)
            )
        else:
            flatpages = FlatPage.objects.filter(url__startswith="/docs/").annotate(
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
