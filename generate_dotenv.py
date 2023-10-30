from pathlib import Path

from django.core.management.utils import get_random_secret_key

DIR = Path(__file__).resolve().parent

with open(Path(DIR / ".env"), "w") as f:
    f.write("DEBUG=True\n")
    f.write("SECRET_KEY=" + get_random_secret_key() + "\n")
    f.write("DATABASE_URL=sqlite://dj5-starter/db.sqlite3\n")
    f.write("EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend\n")
    f.write("STATIC_ROOT=/path/to/your/static_app\n")
    f.write("STATIC_URL=/static/\n")
    f.write("MEDIA_ROOT=/path/to/your/static_app\n")
    f.write("MEDIA_URL=/media/")
f.close()
