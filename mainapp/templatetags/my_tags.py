from django import template
from django.conf import settings
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter()
def email_link(email):
    return mark_safe(f'<a href="mailto:{email}">{email}</a>')


@register.filter()
def with_currency(price):
    return mark_safe(f'{round(price)}&nbsp;{settings.CURRENCY_SYMBOL}') if price else ''


@register.filter()
def get_total_quantity(items):
    return sum([x.quantity for x in items])


@register.filter()
def get_total_cost(items):
    return sum([x.product_cost for x in items])
