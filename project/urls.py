"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.flatpages import views as fp_views
from django.contrib.flatpages.sitemaps import FlatPageSitemap
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path, re_path
from django.utils.translation import gettext_lazy as _

from users.views import (
    ContactFormView,
    HTMXLoginView,
    HTMXLogoutView,
    HTMXSignupView,
    TestedEmailView,
    TestedPasswordChangeView,
    TestedPasswordResetView,
    TestedPasswordSetView,
    avatar_display_create,
    avatar_update_delete,
    profile_update_delete,
)

from .views import home, nav_bar, search_box, search_results

# from django.views.generic import RedirectView


sitemaps = {
    "flatpages": FlatPageSitemap,
}

urlpatterns = [
    path("admin/", admin.site.urls),
    path("i18n/", include("django.conf.urls.i18n")),
    path("accounts/login/", HTMXLoginView.as_view(), name="account_login"),
    path("accounts/logout/", HTMXLogoutView.as_view(), name="account_logout"),
    path("accounts/signup/", HTMXSignupView.as_view(), name="account_signup"),
    path("accounts/contact/", ContactFormView.as_view(), name="account_contact"),
    path("accounts/profile/", profile_update_delete, name="account_profile"),
    path(
        "accounts/password/change/",
        TestedPasswordChangeView.as_view(),
        name="password_change",
    ),
    path(
        "accounts/password/set/", TestedPasswordSetView.as_view(), name="password_set"
    ),
    path(
        "accounts/password/reset/",
        TestedPasswordResetView.as_view(),
        name="password_reset",
    ),
    path("accounts/email/", TestedEmailView.as_view(), name="account_email"),
    path("accounts/avatar/", avatar_display_create, name="avatar_display"),
    path("accounts/avatar/update/", avatar_update_delete, name="avatar_update"),
    path("accounts/", include("allauth.urls")),
    path("__debug__/", include("debug_toolbar.urls")),
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
    path("tinymce/", include("tinymce.urls")),
    path("nav-bar/", nav_bar, name="nav_bar"),
    path("search-box/", search_box, name="search_box"),
]

urlpatterns += i18n_patterns(
    path(_("search/"), search_results, name="search_results"),
    path("", home, name="home"),
    path(_("geocad/"), include("djeocadengine.urls", namespace="djeocadengine")),
)

urlpatterns += [
    re_path(r"^(?P<url>.*/)$", fp_views.flatpage),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
