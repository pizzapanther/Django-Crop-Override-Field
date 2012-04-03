import os

from django.contrib import admin
from django.conf import settings

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
        xf = float(orig.width) / float(crop_data[4])
        yf = float(orig.height) / float(crop_data[5])
        
        box = (int(xf * int(crop_data[0])), int(yf * int(crop_data[1])), int(xf * int(crop_data[2])), int(yf * int(crop_data[3])))
        
        c = Image.open(orig.path)
        c = c.crop(box)
        c.load()
        
        root, ext = os.path.splitext(orig.path)
        cp = root + '_jcrop_' + f.aspect + '.png'
        
        c.save(cp, "PNG")
        rp = cp.replace(settings.MEDIA_ROOT, '')
        if rp.startswith('/'):
          rp = rp[1:]
          
        setattr(obj, f.name, unicode(rp))
        
class CropAdmin (admin.ModelAdmin):
  def save_model (self, request, obj, form, change):
    super(CropAdmin, self).save_model(request, obj, form, change)
    save_crops(obj, request)
    obj.save()
    