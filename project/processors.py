from django.utils.timezone import now

from users.models import Logo


def get_navbar_footer_data(request):
    logo = Logo.objects.first()
    links = "Bar"
    this_year = now().date().year
    return {
        "logo": logo,
        "f_links": links,
        "this_year": this_year,
    }
