from io import StringIO

from django.conf import settings
from django.contrib.flatpages.models import FlatPage
from django.core.management import call_command
from django.test import TestCase, override_settings
from django.urls import reverse

from users.models import User

pword = settings.DJANGO_SUPERUSER_PASSWORD


class PendingMigrationsTests(TestCase):
    """Copy/paste from 'Boost your Django DX', by Adam Johnson"""

    def test_no_pending_migrations(self):
        print("\nTest pending migrations")
        out = StringIO()
        try:
            call_command(
                "makemigrations",
                "--dry-run",
                "--check",
                stdout=out,
                stderr=StringIO(),
            )
        except SystemExit:  # pragma: no cover
            raise AssertionError("Pending migrations:\n" + out.getvalue()) from None


@override_settings(USE_I18N=False)
class ProjectViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        print("\nTest project views")

    def test_home_view_no_htmx(self):
        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)
        print("\n-Test home no htmx status 200")

        self.assertTemplateUsed(response, "home.html")
        print("\n-Test home no htmx template")

    def test_home_view(self):
        response = self.client.get(reverse("home"), headers={"HX-Request": "true"})
        self.assertEqual(response.status_code, 200)
        print("\n-Test home status 200")

        self.assertTemplateUsed(response, "htmx/home.html")
        print("\n-Test home template")

    def test_navbar_view(self):
        response = self.client.get(reverse("nav_bar"), headers={"HX-Request": "true"})
        self.assertEqual(response.status_code, 200)
        print("\n-Test navbar status 200")

        self.assertTemplateUsed(response, "navbar.html")
        print("\n-Test navbar template")

    def test_navbar_view_no_htmx(self):
        response = self.client.get(reverse("nav_bar"))
        self.assertEqual(response.status_code, 302)
        print("\n-Test navbar no htmx status 302")

    def test_searchbox_view(self):
        response = self.client.get(
            reverse("search_box"), headers={"HX-Request": "true"}
        )
        self.assertEqual(response.status_code, 200)
        print("\n-Test searchbox status 200")

        self.assertTemplateUsed(response, "htmx/searchbox.html")
        print("\n-Test searchbox template")


@override_settings(USE_I18N=False)
class SearchTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        print("\nTest search views")
        FlatPage.objects.create(
            id=1,
            title="Flat Page",
            url="/en/docs/flat-page/",
            content="foo",
        )
        FlatPage.objects.create(
            id=2,
            title="Pagina piatta",
            url="/it/documenti/pagina-piatta/",
            content="bar",
        )
        User.objects.create_superuser("boss", "boss@example.com", pword)

    def test_search_results_view_status_code(self):
        response = self.client.get(reverse("search_results") + "?lang=en&q=foo")
        self.assertEqual(response.status_code, 200)
        # just for coverage
        response = self.client.get(reverse("search_results") + "?lang=it&q=bar")
        self.assertEqual(response.status_code, 200)
        print("\n-Test search status 200")

        self.assertTemplateUsed(response, "search_results.html")
        print("\n-Test search template")

        self.assertTrue(response.context["success"])
        print("\n-Test search success")

        response = self.client.get(reverse("search_results") + "?lang=en&q=")
        self.assertFalse(response.context["success"])
        print("\n-Test search not validating")

        response = self.client.get(reverse("search_results") + "?lang=en&q=false")
        self.assertFalse(response.context["success"])
        print("\n-Test search no success")

    def test_search_results_view_context_posts(self):
        page = FlatPage.objects.filter(title="Flat Page")
        response = self.client.get(reverse("search_results") + "?lang=en&q=foo")
        # workaround found in
        # https://stackoverflow.com/questions/17685023/
        # how-do-i-test-django-querysets-are-equal
        self.assertQuerySetEqual(
            response.context["flatpages"], page, transform=lambda x: x
        )
        print("\n-Test search equal querysets")

    def test_super_user_change_flatpage(self):
        self.client.login(username="boss", password=pword)
        # just for coverage
        response = self.client.get("/admin/flatpages/flatpage/1/change/")
        self.assertEqual(response.status_code, 200)
        print("\n-Super can change FlatPage")
