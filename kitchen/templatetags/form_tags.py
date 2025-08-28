from django import template
from django.forms import BoundField

register = template.Library()


@register.filter(name='add_class')
def add_class(
    field: BoundField | object,
    css_class: str,
) -> BoundField | object:

    try:
        return field.as_widget(attrs={"class": css_class})
    except AttributeError:
        return field
