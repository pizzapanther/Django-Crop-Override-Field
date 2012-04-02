Django Crop Override Field provides an additional Django database field for 
helping with defining crops.

### Use Case: ###
You want users to upload an image and on the frontend of your site you display
the image as a square and landscape aspect ratio thumbnails.  You would like 
these thumbnails to be generated automatically from the original. However,
sometimes your auto-cropper doesn't get it right and you would like to provide 
a manual override.

### What Django Override Crop Field does: ###
*  Gives you an optional image field to store your crop in.
When not used it falls back to providing the original image to be resized.

*  An admin widget to make quick crops right in the admin interface.


### Usage: ###
#### models.py ####
```python
from django.db import models

from crop_override import CropOverride, OriginalImage

class Image (models.Model):
  alt_tag = models.CharField('Alt Tag', max_length=75)
  
  full_size = OriginalImage('Full Size Original', upload_to='some/dir')
  
  square_crop = CropOverride('Square Crop, 1x1 Ratio', upload_to='some/dir', original='full_size', aspect='1x1')
  landscape_crop = CropOverride('Landscape Crop, 4x3 Ratio', upload_to='some/dir', original='full_size', aspect='4x3')
  portrait_crop = CropOverride('Portrait Crop, 3x4 Ratio', upload_to='some/dir', original='full_size', aspect='3x4')
  
```

#### admin.py ####
```python
from crop_override.admin import CropAdmin

class ImageAdmin (CropAdmin):
  ...
  
```

#### views.py ####
```python

from crop_override import get_override
#get_override returns crop field or original

def some_view (request):
  ...
  
  im = Image.objects.get(id=some_id)
  
  image_for_square_use = get_override(im, 'square_crop'))
  image_for_landscape_use = get_override(im, 'landscape_crop'))
  image_for_portrait_use = get_override(im, 'portrait_crop'))
  
  ...
  
```

#### some_template.html Using Sorl Thumbnail ####
```html
{% load crop_util thumbnail %}
<!--get_override returns crop field or original-->

{% thumbnail model_instance|get_override:'square_crop' "400x400" crop="center" as square %}
<p>
  Square Image: <img alt="{{ model_instance.alt }}" src="{{ square.url }}">
</p>
{% endthumbnail %}

{% thumbnail model_instance|get_override:'landscape_crop' "400x300" crop="center" as landscape %}
<p>
  Landscape Image: <img alt="{{ model_instance.alt }}" src="{{ landscape.url }}">
</p>
{% endthumbnail %}

{% thumbnail model_instance|get_override:'portrait_crop' "300x400" crop="center" as portrait %}
<p>
  Portrait Image: <img alt="{{ model_instance.alt }}" src="{{ portrait.url }}">
</p>
{% endthumbnail %}

```
