from users.models import Logo


def get_navbar_footer_data(request):
    logo = Logo.objects.first()
    links = "Bar"
    return {"logo": logo, "f_links": links}
