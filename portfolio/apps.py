from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.utils.translation import gettext as _


def create_portfolio_group(sender, **kwargs):
    from django.contrib.auth.models import Group, Permission

    grp, created = Group.objects.get_or_create(name=_("Project Manager"))
    if created:
        permissions = Permission.objects.filter(
            codename__in=(
                "view_project",
                "add_project",
                "change_project",
                "delete_project",
            )
        )
        grp.permissions.set(permissions)


def create_activities(sender, **kwargs):
    from .choices import ACTIVITY
    from .models import Activity

    for activity in ACTIVITY:
        act, created = Activity.objects.get_or_create(
            full=activity[1],
            abbrev=activity[0],
        )


class PortfolioConfig(AppConfig):
    name = "portfolio"

    def ready(self):
        post_migrate.connect(create_portfolio_group, sender=self)
        # post_migrate.connect(create_activities, sender=self)
