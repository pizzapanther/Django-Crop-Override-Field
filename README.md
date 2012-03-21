Django Crop Override Field provides an additional Django database field for 
helping with defining crops.

### Use Case: ###
You want users to upload an image and on the frontend of your site you display
the image as a square and landscape aspect ratio thumbnails.  You would like 
these thumbnails to be generated automatically from the original, but sometimes
your auto-cropper doesn't get it right and you would like to provide a manual
override.

### What Django Override Crop Field does: ###
*  Gives you an optional image field to store your crop in.
When not used it falls back to providing the original image to be resized.

*  An admin widget to make quick crops right in the admin interface.


### Usage ###
#### models.py ####
```python
from django.db import models

from crop_override import CropOverride

class Image (models.Model):
  alt_tag = models.CharField('Alt Tag', max_length=75)
  
  full_size = models.ImageField('Full Size Original', upload_to='some/dir')
  
  square_crop = CropOverride('Square Crop, 1x1 Ratio', upload_to='some/dir', original='full_size', aspect='1x1')
  landscape_crop = CropOverride('Landscape Crop, 4x3 Ratio', upload_to='some/dir', original='full_size', aspect='4x3')
  portrait_crop = CropOverride('Portrait Crop, 3x4 Ratio', upload_to='some/dir', original='full_size', aspect='3x4')
  
```

#### views.py ####
```python

def some_view (request):
  ...
  
  im = Image.objects.get(id=some_id)
  process_square(im.square_crop)
  process_landscape(im.landscape_crop)
  process_portrait(im.portrait_crop)
  
  ...
  
```

#### some_template.html Using Sorl Thumbnail ####
```html
{% load thumbnail %}
{% thumbnail some_image.square_crop "400x400" crop="center" as square %}
<p>
  Square Image: <img alt="{{ some_image.alt }}" src="{{ square.url }}">
</p>
{% endthumbnail %}

{% thumbnail some_image.landscape_crop "400x300" crop="center" as landscape %}
<p>
  Landscape Image: <img alt="{{ some_image.alt }}" src="{{ landscape.url }}">
</p>
{% endthumbnail %}

{% thumbnail some_image.portrait_crop "300x400" crop="center" as portrait %}
<p>
  Portrait Image: <img alt="{{ some_image.alt }}" src="{{ portrait.url }}">
</p>
{% endthumbnail %}

```
