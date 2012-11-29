import os
import time
from cStringIO import StringIO

from django.contrib import admin
from django.conf import settings
from django.core.files.base import ContentFile

import Image

from .field import CropOverride

def save_crops (obj, request):
  for f in obj._meta.fields:
    if isinstance(f, CropOverride):
      crop_data = request.REQUEST.get('crop_' + f.name, '')
      if crop_data:
        crop_data = crop_data.split(',')
        if crop_data[4] == 0 or crop_data[5] == 0:
          continue
        
        if int(crop_data[2]) - int(crop_data[0]) == 0 or int(crop_data[3]) - int(crop_data[1]) == 0:
          continue
        
        orig = getattr(obj, f.original)
        buf = StringIO(orig.read())
        c = Image.open(buf)
        width, height = c.size
        
        xf = float(width) / float(crop_data[4])
        yf = float(height) / float(crop_data[5])
        
        box = (int(xf * int(crop_data[0])), int(yf * int(crop_data[1])), int(xf * int(crop_data[2])), int(yf * int(crop_data[3])))
        
        root, ext = os.path.splitext(orig.name)
        cp = root + '_jcrop_' + f.aspect + time.strftime("_%a%d%b%Y%H%M%S", time.localtime()) + '.png'
        
        c = c.crop(box)
        c.load()
        
        buf = StringIO()
        c.save(buf, "PNG")
        
        thumb_field = getattr(obj, f.name)
        cp = thumb_field.storage.save(cp, ContentFile(buf.getvalue()))
        setattr(obj, f.name, cp)
        
class CropAdmin (admin.ModelAdmin):
  def save_model (self, request, obj, form, change):
    super(CropAdmin, self).save_model(request, obj, form, change)
    save_crops(obj, request)
    obj.save()
    
