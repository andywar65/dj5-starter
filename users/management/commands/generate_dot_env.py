from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.core.management.utils import get_random_secret_key


class Command(BaseCommand):
    help = "Generate dot env file."

    def handle(self, *args, **options):
        if settings.DEBUG is False:
            raise CommandError("This command cannot be run when DEBUG is False.")

        self.stdout.write("Generating .env file...")

        create_item()

        self.stdout.write(
            """Done.\n
            Remember that this is a dummy installation, it works on a Sqlite database.\n
            Create a Postgres database, update dotenv file\n
            (update db.url and media/static roots) then migrate.
            """
        )


def create_item():
    with open(Path(settings.BASE_DIR / ".env"), "w") as f:
        f.write("DEBUG=True\n")
        f.write("SECRET_KEY=" + get_random_secret_key() + "\n")
        f.write("DATABASE_URL=sqlite://dj5-starter/db.sqlite3\n")
        f.write("EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend\n")
        f.write("STATIC_ROOT=/path/to/your/static_app\n")
        f.write("STATIC_URL=/static/\n")
        f.write("MEDIA_ROOT=/path/to/your/media_app\n")
        f.write("MEDIA_URL=/media/")
    f.close()
