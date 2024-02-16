from django.urls import path
from django.utils.translation import gettext_lazy as _

from .views import (
    ProjectCategoryListView,
    ProjectDetailView,
    ProjectListAllView,
    ProjectListMapView,
    ProjectListView,
    ProjectYearArchiveView,
)

app_name = "portfolio"
urlpatterns = [
    path(_("selected/"), ProjectListView.as_view(), name="project_list"),
    path(_("all/"), ProjectListAllView.as_view(), name="project_list_all"),
    path(_("map/"), ProjectListMapView.as_view(), name="project_map"),
    path("<int:year>/", ProjectYearArchiveView.as_view(), name="year"),
    path(_("category/"), ProjectCategoryListView.as_view(), name="project_category"),
    path("<slug>/", ProjectDetailView.as_view(), name="project_detail"),
]
