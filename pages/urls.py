from django.urls import path

from .views import ShotgunCreateFormView, ShotgunDetailView

app_name = "pages"
urlpatterns = [
    # path("shotgun/", ShotgunArchiveIndexView.as_view(), name="shotgun_index"),
    path(
        "<int:pk>/",
        ShotgunDetailView.as_view(),
        name="shotgun_detail",
    ),
    path(
        "add/",
        ShotgunCreateFormView.as_view(),
        name="shotgun_create",
    ),
]
