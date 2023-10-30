from pathlib import Path

from django.core.management.utils import get_random_secret_key

DIR = Path(__file__).resolve().parent

with open(Path(DIR / ".env"), "w") as f:
    f.write("DEBUG=True")
    f.write("SECRET_KEY=" + get_random_secret_key())
    f.write("DATABASE_URL=postgres://USER:PASSWORD@HOST:PORT/NAME")
    f.write("EMAIL_BACKEND=")
    f.write("STATIC_ROOT=/path/to/your/static_app")
    f.write("STATIC_URL=/static/")
    f.write("MEDIA_ROOT=/path/to/your/static_app")
    f.write("MEDIA_URL=/media/")
f.close()
