from django import template

register = template.Library()

@register.filter
def get_override (instance, crop_field):
  crop = getattr(instance, crop_field)
  if crop:
    return crop
    
  for f in instance._meta.fields:
    if f.name == crop_field:
      return getattr(instance, f.original)
      
  return None
  