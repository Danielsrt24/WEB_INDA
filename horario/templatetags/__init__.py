from django import template

register = template.Library()

@register.filter
def dict_lookup(dictionary, key):
    """Permite acceder a un diccionario por clave en el template."""
    if isinstance(dictionary, dict):
        return dictionary.get(key, 'Desconocido')
    return ''