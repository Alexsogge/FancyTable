from django import template


register = template.Library()

@register.filter
def get_icon_path(icon_name):
    return "icons/{}".format(icon_name)