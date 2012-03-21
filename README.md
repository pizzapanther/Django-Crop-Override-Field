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
  first_name = models.CharField(max_length=30)
  
```
