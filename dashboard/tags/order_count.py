from atexit import register
from django import template
from dashboard.models import Order

register = template.Library()

@register.filter
def order_item_count(user):
    qs = Order.objects.filter(ordered=False)
    if qs.exists():
        return qs[0].items.count()
    