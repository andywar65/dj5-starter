import uuid

from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.models import AbstractUser, Permission
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import gettext_lazy as _
from filer.fields.image import FilerImageField


class User(AbstractUser):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)
        if self.is_active:
            p, created = Profile.objects.get_or_create(user_id=self.uuid)
            if created:
                content_type = ContentType.objects.get_for_model(Profile)
                permission = Permission.objects.get(
                    codename="change_profile",
                    content_type=content_type,
                )
                self.user_permissions.add(permission)

    def get_full_name(self):
        if self.profile.anonymize:
            return self.username
        elif self.first_name and self.last_name:
            return self.first_name + " " + self.last_name
        else:
            return self.username

    def get_short_name(self):
        if self.profile.anonymize:
            return self.username
        elif self.first_name:
            return self.first_name
        else:
            return self.username

    def get_avatar(self):
        if self.profile.anonymize:
            return
        elif self.profile.image:
            return True
        # attempts to retrieve avatar from social account
        try:
            s = SocialAccount.objects.get(user_id=self.uuid)
            return s.get_avatar_url()
        except SocialAccount.DoesNotExist:
            return

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")
        ordering = (
            "first_name",
            "last_name",
            "username",
        )


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True, editable=False
    )
    # "avatar" field is just used to upload and validate images,
    # then file is saved as "image" field
    avatar = models.ImageField(null=True)
    image = FilerImageField(
        null=True, blank=True, related_name="profile_image", on_delete=models.SET_NULL
    )
    bio = models.TextField(_("Short bio"), null=True, blank=True)
    anonymize = models.BooleanField(
        _("Anonymize"),
        default=False,
        help_text=_("Anonymize your account in public pages"),
    )

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = _("Profile")
        verbose_name_plural = _("Profiles")


class UserMessage(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="user_message",
        verbose_name=_("User"),
    )
    subject = models.CharField(
        max_length=200,
        verbose_name=_("Subject"),
    )
    body = models.TextField(
        verbose_name=_("Text"),
    )

    def __str__(self):
        return _("Message - %(id)d") % {"id": self.id}

    class Meta:
        verbose_name = _("Message")
        verbose_name_plural = _("Messages")


class Logo(models.Model):
    name = models.CharField(_("Name"), max_length=255)
    image = FilerImageField(
        null=True, blank=True, related_name="logo_image", on_delete=models.SET_NULL
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Logo")
        verbose_name_plural = _("Logos")


class FooterLink(models.Model):
    title = models.CharField(
        _("Title"),
        max_length=50,
    )
    link = models.URLField(
        _("Link"),
        max_length=200,
    )

    class Meta:
        verbose_name = _("Footer link")
        verbose_name_plural = _("Footer links")
