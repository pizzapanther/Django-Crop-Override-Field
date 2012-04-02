from django import forms
from django.db import models
from django.utils.text import capfirst
from django.contrib.admin.widgets import AdminFileWidget

from crop_override.widget import CropOverrideInput, AdminCropOverrideInput, OriginalInput, AdminOriginalInput

class CropOverrideField (forms.ImageField):
  widget = CropOverrideInput
  
  def __init__ (self, original, aspect, **kwargs):
    self.original = original
    self.aspect = aspect
    
    if kwargs.has_key('widget'):
      #override default admin widget
      if kwargs['widget'] == AdminFileWidget:
        kwargs['widget'] = AdminCropOverrideInput
        
      if isinstance(kwargs['widget'], type):
        kwargs['widget'] = kwargs['widget'](self.original, self.aspect)
        
    else:
      kwargs['widget'] = self.widget(self.original, self.aspect)
      
    super(CropOverrideField, self).__init__(**kwargs)
    
class OriginalField (forms.ImageField):
  widget = OriginalInput
  
  def __init__ (self, *args, **kwargs):
    if kwargs.has_key('widget'):
      #override default admin widget
      if kwargs['widget'] == AdminFileWidget:
        kwargs['widget'] = AdminOriginalInput
        
    super(OriginalField, self).__init__(*args, **kwargs)
    
class CropOverride (models.ImageField):
  def __init__ (self, *args, **kwargs):
    self.original = kwargs['original']
    del kwargs['original']
    
    self.aspect = kwargs['aspect']
    del kwargs['aspect']
    
    if not kwargs.has_key('blank'):
      kwargs['blank'] = True
      
    if not kwargs.has_key('null'):
      kwargs['null'] = True
      
    super(CropOverride, self).__init__(*args, **kwargs)
    
  def custom_formfield(self, form_class=CropOverrideField, **kwargs):
    defaults = {'required': not self.blank,
                'label': capfirst(self.verbose_name),
                'help_text': self.help_text}
    if self.has_default():
      if callable(self.default):
        defaults['initial'] = self.default
        defaults['show_hidden_initial'] = True
        
      else:
        defaults['initial'] = self.get_default()
        
    defaults.update(kwargs)
    return form_class(self.original, self.aspect, **defaults)
    
  def formfield (self, **kwargs):
    defaults = {'form_class': CropOverrideField}
    defaults.update(kwargs)
    
    return self.custom_formfield(**defaults)
    
class OriginalImage (models.ImageField):
  def formfield (self, **kwargs):
    defaults = {'form_class': OriginalField}
    defaults.update(kwargs)
    return super(OriginalImage, self).formfield(**defaults)
