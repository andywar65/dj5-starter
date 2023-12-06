from pathlib import Path

from django.core.management.utils import get_random_secret_key

DIR = Path(__file__).resolve().parent

with open(Path(DIR / ".env"), "w") as f:
    f.write("DEBUG=True\n")
    f.write("SECRET_KEY=" + get_random_secret_key() + "\n")
    f.write("# change database url and uncomment it\n")
    f.write("# then run migrations and create superuser again\n")
    f.write("# DATABASE_URL=postgres://postgres:postgres@db:5432/postgres\n")
    f.write("EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend\n")
    f.write("# change static and media roots\n")
    f.write("STATIC_ROOT=/path/to/your/static_app\n")
    f.write("STATIC_URL=/static/\n")
    f.write("MEDIA_ROOT=/path/to/your/media_app\n")
    f.write("MEDIA_URL=/media/\n")
    f.write("# change superuser data\n")
    f.write("DJANGO_SUPERUSER_USERNAME=andywar65\n")
    f.write("DJANGO_SUPERUSER_EMAIL=andy.war1965@gmail.com\n")
    f.write("DJANGO_SUPERUSER_PASSWORD=P4s5W0r6")
f.close()
