from allauth.account.models import EmailAddress
from allauth.account.views import (
    EmailView,
    LoginView,
    LogoutView,
    PasswordChangeView,
    PasswordResetView,
    PasswordSetView,
    SignupView,
)
from allauth.socialaccount.models import SocialAccount
from django.conf import settings
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.core.mail import EmailMessage
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views.generic.edit import FormView

from project.views import check_htmx_request

from .forms import AvatarChangeForm, ContactForm, ProfileChangeForm
from .models import UserMessage


class HxTemplateMixin:
    """Switches template depending on request.htmx"""

    def get_template_names(self):
        if not self.request.htmx:
            return [self.template_name.replace("htmx/", "")]
        else:
            return [self.template_name]


class TestedPasswordChangeView(
    PermissionRequiredMixin, HxTemplateMixin, PasswordChangeView
):
    template_name = "account/htmx/password_change.html"
    permission_required = "users.change_profile"


class TestedPasswordSetView(
    PermissionRequiredMixin,
    PasswordSetView,
):
    template_name = "account/htmx/password_set.html"
    permission_required = "users.change_profile"


class TestedPasswordResetView(
    HxTemplateMixin,
    PasswordResetView,
):
    template_name = "account/htmx/password_reset.html"

    def setup(self, request, *args, **kwargs):
        super(TestedPasswordResetView, self).setup(request, *args, **kwargs)
        if request.user.is_authenticated:
            if not request.user.has_perm("users.change_profile"):
                raise PermissionDenied


class TestedEmailView(
    PermissionRequiredMixin,
    EmailView,
):
    template_name = "account/htmx/email.html"
    permission_required = "users.change_profile"


class HTMXLoginView(HxTemplateMixin, LoginView):
    template_name = "account/htmx/login.html"


class HTMXLogoutView(HxTemplateMixin, LogoutView):
    template_name = "account/htmx/logout.html"


class HTMXSignupView(HxTemplateMixin, SignupView):
    template_name = "account/htmx/signup.html"


@permission_required("users.change_profile")
def avatar_display_create(request):
    check_htmx_request(request)
    user = request.user
    context = {"user": user}
    template_name = "account/htmx/avatar_display.html"
    if request.method == "GET" and "create" in request.GET:
        template_name = "account/htmx/avatar_create.html"
        form = AvatarChangeForm()
        context = {"form": form}
    elif request.method == "POST":
        form = AvatarChangeForm(request.POST, request.FILES)
        if form.is_valid():
            # assign profile form fields
            profile = user.profile
            profile.avatar = form.cleaned_data["avatar"]
            profile.save()
            return HttpResponseRedirect(
                reverse("avatar_display") + "?submitted=True",
            )
        context = {"form": form}
        template_name = "account/htmx/avatar_create.html"
    elif request.method == "GET" and "submitted" in request.GET:
        return TemplateResponse(
            request,
            template_name,
            context,
            headers={"HX-Trigger": "refreshNavbar"},
        )
    return TemplateResponse(
        request,
        template_name,
        context,
    )


@permission_required("users.change_profile")
def avatar_update_delete(request):
    check_htmx_request(request)
    user = request.user
    context = {"user": user}
    template_name = "account/htmx/avatar_update.html"
    if request.method == "DELETE":
        profile = user.profile
        profile.avatar = None
        profile.save()
        template_name = "account/htmx/avatar_display.html"
        # SocialAccount.objects.filter(user_id=user.uuid).delete()
        return TemplateResponse(
            request,
            template_name,
            context,
            headers={"HX-Trigger": "refreshNavbar"},
        )
    elif request.method == "PUT":
        template_name = "account/htmx/avatar_display.html"
    elif request.method == "POST":
        form = AvatarChangeForm(request.POST, request.FILES)
        if form.is_valid():
            # assign profile form fields
            profile = user.profile
            profile.avatar = form.cleaned_data["avatar"]
            profile.save()
            return HttpResponseRedirect(
                reverse("avatar_display") + "?submitted=True",
            )
    else:
        form = AvatarChangeForm(
            initial={
                "avatar": user.profile.avatar,
            }
        )
    context["form"] = form
    return TemplateResponse(
        request,
        template_name,
        context,
    )


@permission_required("users.change_profile")
def profile_update_delete(request):
    user = request.user
    if request.method == "DELETE":
        check_htmx_request(request)
        user.is_active = False
        user.first_name = ""
        user.last_name = ""
        user.email = ""
        user.save()
        profile = user.profile
        profile.avatar = None
        profile.bio = ""
        profile.save()
        EmailAddress.objects.filter(user_id=user.uuid).delete()
        SocialAccount.objects.filter(user_id=user.uuid).delete()
        template_name = "account/htmx/account_delete.html"
        context = {}
        return TemplateResponse(
            request,
            template_name,
            context,
            headers={"HX-Trigger": "refreshNavbar"},
        )
    elif request.method == "POST":
        form = ProfileChangeForm(request.POST)
        if form.is_valid():
            # assign user form fields
            user.first_name = form.cleaned_data["first_name"]
            user.last_name = form.cleaned_data["last_name"]
            user.email = form.cleaned_data["email"]
            user.save()
            # assign profile form fields
            profile = user.profile
            profile.bio = form.cleaned_data["bio"]
            profile.anonymize = form.cleaned_data["anonymize"]
            profile.save()
            return HttpResponseRedirect(
                reverse("account_profile") + "?submitted=True",
            )
    else:
        form = ProfileChangeForm(
            initial={
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "bio": user.profile.bio,
                "anonymize": user.profile.anonymize,
            }
        )
    if request.htmx:
        template_name = "account/htmx/account_profile.html"
    else:
        template_name = "account/account_profile.html"
    context = {"form": form}
    if request.method == "GET" and "submitted" in request.GET:
        context["submitted"] = True
        return TemplateResponse(
            request,
            template_name,
            context,
            headers={"HX-Trigger": "refreshNavbar"},
        )
    return TemplateResponse(request, template_name, context)


class ContactFormView(PermissionRequiredMixin, HxTemplateMixin, FormView):
    form_class = ContactForm
    template_name = "account/htmx/contact.html"
    permission_required = "users.change_profile"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if "submitted" in self.request.GET:
            context["submitted"] = True
        return context

    def form_valid(self, form):
        subject = form.cleaned_data["subject"]
        body = form.cleaned_data["body"]
        user = self.request.user
        UserMessage.objects.create(user_id=user.uuid, subject=subject, body=body)
        recipient = settings.EMAIL_RECIPIENT
        msg = "%(body)s\n\n%(from)s: %(full)s (%(email)s)" % {
            "body": body,
            "from": _("From"),
            "full": user.get_full_name(),
            "email": user.email,
        }
        mailto = [
            recipient,
        ]
        email = EmailMessage(subject, msg, settings.SERVER_EMAIL, mailto)
        email.send()
        return super(ContactFormView, self).form_valid(form)

    def get_success_url(self):
        return reverse("account_contact") + "?submitted=True"
