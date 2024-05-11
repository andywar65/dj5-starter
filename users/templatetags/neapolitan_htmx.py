from django import template
from django.utils.safestring import mark_safe
from neapolitan.views import Role

register = template.Library()


def action_links(view, object):
    actions = [
        (Role.DETAIL.reverse(view, object), "View"),
        (Role.UPDATE.reverse(view, object), "Edit"),
        (Role.DELETE.reverse(view, object), "Delete"),
    ]
    # adding htmx links
    links = [
        f"<a class='link link-primary' hx-get='{url}'"
        f"hx-target='#content' hx-push-url='true'>{anchor_text}</a>"
        for url, anchor_text in actions
    ]
    return mark_safe(" | ".join(links))


@register.inclusion_tag("neapolitan/partial/list.html")
def object_list_htmx(objects, view):
    """
    Renders a list of objects with the given fields.

    Inclusion tag usage::

        {% object_list objects view %}

    Template: ``neapolitan/partial/list.html`` — Will render a table of objects
    with links to view, edit, and delete views.
    """

    fields = view.fields
    headers = [objects[0]._meta.get_field(f).verbose_name for f in fields]
    object_list = [
        {
            "object": object,
            "fields": [
                object._meta.get_field(f).value_to_string(object) for f in fields
            ],
            "actions": action_links(view, object),
        }
        for object in objects
    ]
    return {
        "headers": headers,
        "object_list": object_list,
    }
