from django import forms
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _

from .models import Profile, UserMessage


class AvatarChangeForm(ModelForm):
    class Meta:
        model = Profile
        fields = [
            "avatar",
        ]
        widgets = {"avatar": forms.FileInput()}


class ProfileChangeForm(forms.Form):
    first_name = forms.CharField(
        label=_("First name"), required=False, widget=forms.TextInput()
    )
    last_name = forms.CharField(
        label=_("Last name"), required=False, widget=forms.TextInput()
    )
    email = forms.EmailField(
        label=_("Email"),
        required=True,
        widget=forms.EmailInput(
            attrs={"autocomplete": "email", "placeholder": "you@example.com"}
        ),
    )
    bio = forms.CharField(
        label=_("Short bio"),
        required=False,
        widget=forms.Textarea(attrs={"placeholder": _("Talk about yourself")}),
    )
    anonymize = forms.BooleanField(
        label=_("Check to show only username"),
        required=False,
    )


class ContactForm(ModelForm):
    class Meta:
        model = UserMessage
        fields = (
            "subject",
            "body",
        )
        widgets = {
            "subject": forms.TextInput(
                attrs={"placeholder": _("Write here the subject")}
            ),
            "body": forms.Textarea(attrs={"placeholder": _("Write here the message")}),
        }
