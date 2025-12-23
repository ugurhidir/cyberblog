import markdown
from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter(name='markdown')
def markdown_format(text):
    # fenced_code: ``` ile kod yazmayı sağlar
    # codehilite: Kodları renklendirilebilir hale getirir
    return mark_safe(markdown.markdown(text, extensions=['fenced_code', 'codehilite']))