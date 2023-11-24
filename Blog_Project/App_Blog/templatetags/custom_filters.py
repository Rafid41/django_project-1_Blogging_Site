from django import template

register = template.Library()

def range_filter(value):
    return value[0:500] + '.............'


# register('name_to_call', filter_function)
register.filter('range_filter', range_filter)