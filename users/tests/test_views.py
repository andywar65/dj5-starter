from pathlib import Path

from allauth.account.models import EmailAddress
from django.conf import settings
from django.contrib.auth.models import Permission
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse

from project.views import HxCRUDView
from users.models import FooterLink, User

pword = settings.DJANGO_SUPERUSER_PASSWORD


class FooterLinkView(HxCRUDView):
    model = FooterLink
    fields = ["title", "link"]


urlpatterns = [
    *FooterLinkView.get_urls(),
]


@override_settings(USE_I18N=False)
@override_settings(MEDIA_ROOT=Path(settings.MEDIA_ROOT).joinpath("temp"))
class UserViewsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        print("\nTest user views")
        boss = User.objects.create_superuser("boss", "boss@example.com", pword)
        EmailAddress.objects.create(user_id=boss.uuid)
        immutable = User.objects.create_user("immutable", "immu@example.com", pword)
        p = Permission.objects.get(codename="change_profile")
        immutable.user_permissions.remove(p)

    def tearDown(self):
        """Checks existing files, then removes them"""
        try:
            path = Path(settings.MEDIA_ROOT).joinpath("uploads/images/users/")
            list = [e for e in path.iterdir() if e.is_file()]
            for file in list:
                Path(file).unlink()
        except FileNotFoundError:
            pass

    def test_user_views_status_code_302(self):
        print("\n-Test User Views not logged")

        response = self.client.get(reverse("account_profile"))
        self.assertRedirects(
            response,
            reverse("account_login") + "?next=/accounts/profile/",
            status_code=302,
            target_status_code=200,
        )
        print("\n--Test Account Profile redirect")

        response = self.client.get(reverse("account_contact"))
        self.assertRedirects(
            response,
            reverse("account_login") + "?next=/accounts/contact/",
            status_code=302,
            target_status_code=200,
        )
        print("\n--Test Account Contact redirect")

    def test_immutable_user_views_status_code_302(self):
        print("\n-Test Immutable User Views logged")
        self.client.login(username="immutable", password=pword)

        response = self.client.get(reverse("account_profile"))
        self.assertEqual(response.status_code, 302)
        print("\n--Test Immutable Account Profile forbidden")

        response = self.client.get(reverse("account_contact"))
        self.assertEqual(response.status_code, 403)
        print("\n--Test Immutable Account Contact success")

        response = self.client.get(reverse("password_reset"))
        self.assertEqual(response.status_code, 403)
        print("\n--Test Immutable Account can't reset password")

    def test_user_views_status_code_200(self):
        print("\n-Test User Views logged in")
        self.client.login(username="boss", password=pword)

        response = self.client.get(reverse("account_profile"))
        self.assertEqual(response.status_code, 200)
        print("\n--Test Account Profile success")

        response = self.client.get(reverse("account_contact"))
        self.assertEqual(response.status_code, 200)
        print("\n--Test Account Contact success")

    def test_change_account_avatar(self):
        print("\n-Test Add and Delete account avatar")
        self.client.login(username="boss", password=pword)
        img_path = Path(settings.PROJECT_DIR).joinpath("static/tests/image.jpg")
        with open(img_path, "rb") as f:
            content = f.read()

        response = self.client.post(
            reverse("avatar_display"),
            {
                "avatar": SimpleUploadedFile("image.jpg", content, "image/jpg"),
            },
            headers={"HX-Request": "true"},
            follow=True,
        )
        self.assertRedirects(
            response,
            reverse("avatar_display") + "?refresh=True",
            status_code=302,
            target_status_code=200,
        )
        print("\n--Test Add Avatar redirect")

        response = self.client.delete(
            reverse("avatar_update"),
            headers={"HX-Request": "true"},
        )
        self.assertEqual(response.status_code, 200)
        print("\n--Test Delete Avatar status code")

    def test_change_account_profile(self):
        print("\n-Test Change account profile")
        self.client.login(username="boss", password=pword)

        response = self.client.post(
            reverse("account_profile"),
            {
                "first_name": "Gonzo",
                "last_name": "Bilal",
                "email": "gonzo@bilal.com",
                "bio": "My biography",
                "anonymize": False,
            },
            follow=True,
        )
        self.assertRedirects(
            response,
            reverse("account_profile") + "?refresh=True",
            status_code=302,
            target_status_code=200,
        )
        print("\n--Test Info redirect")

    def test_send_account_contact(self):
        print("\n-Test send account contact")
        self.client.login(username="boss", password=pword)

        response = self.client.post(
            reverse("account_contact"),
            {"subject": "Subject", "body": "Message"},
            follow=True,
        )
        self.assertRedirects(
            response,
            reverse("account_contact") + "?submitted=True",
            status_code=302,
            target_status_code=200,
        )
        print("\n--Test send account contact redirect")

    def test_delete_account_profile(self):
        print("\n-Test delete account profile")
        self.client.login(username="boss", password=pword)

        response = self.client.delete(
            reverse("account_profile"),
            headers={"HX-Request": "true"},
        )
        self.assertEqual(response.status_code, 200)
        print("\n--Test delete account profile success")
        self.assertTemplateUsed(response, "account/htmx/account_delete.html")
        print("\n-Test delete account template")


class NeapolitanTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        print("\nTest neapolitan view")
        FooterLink.objects.create(
            id=1,
            title="GitHub",
            link="https://github.com/andywar65",
        )
        FooterLink.objects.create(
            id=2,
            title="digitalkOmiX",
            link="https://digitalkomix.com",
        )

    def test_HxCRUD_view(self):
        response = self.client.get("/footerlink/")
        self.assertEqual(response.status_code, 200)
