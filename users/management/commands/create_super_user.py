from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from users.models import User


class Command(BaseCommand):
    help = "Create superuser."

    def handle(self, *args, **options):
        if settings.DEBUG is False:
            raise CommandError("This command cannot be run when DEBUG is False.")

        self.stdout.write("Creating superuser...")

        create_item()

        self.stdout.write(
            """Done, you can log in as 'andywar65' with pw='P4s5W0r6'.\n
            Remember that this is a dummy installation, it works on a Sqlite database.\n
            Create a Postgres database, update dotenv file (db.url and media/static roots)\n
            then migrate and create a new super user.
            """
        )


def create_item():
    User.objects.create_superuser("andywar65", "andy.war1965@gmail.com", "P4s5W0r6")
