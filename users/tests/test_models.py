from allauth.socialaccount.models import SocialAccount
from django.conf import settings
from django.test import TestCase, override_settings

from users.models import User, UserMessage

pword = settings.DJANGO_SUPERUSER_PASSWORD


@override_settings(LANGUAGE_CODE="en-us")
class UserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        print("\nTest user models")
        # Set up non-modified objects used by all test methods
        user = User.objects.create(
            username="andy.war65",
            password=pword,
            first_name="Andrea",
            last_name="Guerra",
            email="andy@war.com",
        )
        # next save is just for coverage purposes
        user.save()
        SocialAccount.objects.create(
            user_id=user.uuid, provider="google", extra_data={"picture": "foo"}
        )
        profile = user.profile
        profile.bio = "My biography"
        profile.save()
        User.objects.create(username="nonames", password=pword, email="nonames@war.com")
        UserMessage.objects.create(user_id=user.uuid, subject="Foo", body="Bar")
        anonim = User.objects.create(
            username="anonim",
            password=pword,
            first_name="Anonimous",
            last_name="War",
            email="anonim@war.com",
        )
        anonim.profile.anonymize = True
        anonim.profile.save()

    def test_user_get_avatar(self):
        user = User.objects.get(username="andy.war65")
        self.assertEqual(user.get_avatar(), "foo")
        print("\n-Tested User get avatar")

    def test_profile_get_names(self):
        user = User.objects.get(username="andy.war65")
        self.assertEqual(user.profile.__str__(), "andy.war65")
        print("\n-Tested Profile __str__")
        self.assertEqual(user.__str__(), "andy.war65")
        print("\n-Tested User __str__")
        self.assertEqual(user.get_full_name(), "Andrea Guerra")
        print("\n-Tested User full name")
        self.assertEqual(user.get_short_name(), "Andrea")
        print("\n-Tested User short name")

    def test_profile_get_no_names(self):
        user = User.objects.get(username="nonames")
        self.assertEqual(user.profile.__str__(), "nonames")
        print("\n-Tested Profile no __str__")
        self.assertEqual(user.__str__(), "nonames")
        print("\n-Tested User no __str__")
        self.assertEqual(user.get_full_name(), "nonames")
        print("\n-Tested User no full name")
        self.assertEqual(user.get_short_name(), "nonames")
        print("\n-Tested User no short name")

    def test_profile_get_anonimized(self):
        user = User.objects.get(username="anonim")
        self.assertEqual(user.get_full_name(), "anonim")
        print("\n-Tested User anonymous full name")
        self.assertEqual(user.get_short_name(), "anonim")
        print("\n-Tested User anonymous short name")
        self.assertEqual(user.get_avatar(), None)
        print("\n-Tested User no avatar")

    def test_usermessage_get_str(self):
        message = UserMessage.objects.get(subject="Foo")
        self.assertEqual(message.__str__(), "Message - " + str(message.id))
        print("\n-Tested UserMessage __str__")
