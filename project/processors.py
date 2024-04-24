from django.utils.timezone import now

from users.models import FooterLink, Logo


def get_navbar_footer_data(request):
    logo = Logo.objects.first()
    links = FooterLink.objects.all()
    this_year = now().date().year
    return {
        "logo": logo,
        "f_links": links,
        "this_year": this_year,
        "l_code": f"/{request.LANGUAGE_CODE}/",
    }
