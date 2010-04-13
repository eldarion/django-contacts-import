from django import template


register = template.Library()


@register.filter
def contact_selected(session, pk):
    return str(pk) in session.get("selected-contacts", ())
