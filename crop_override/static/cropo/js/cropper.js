var jcrop_api;
var ph = 100;
var pw = 100;
  
function show_cropper (name, orig, aspect) {
  var d = new Date();
  var ts = d.getTime();
  
  ph = 100;
  pw = 100;

  if (aspect > 1) {
    ph = 100 / aspect;
  }
  
  else if (aspect < 1) {
    pw = 100 * aspect;
  }
  
  var img = jQuery('#id_orig_' + orig).val();
  var value = jQuery('#id_'+orig).val();
  if (!img || !!value) {
    // cancel if the value has been changed (field not blank) or no img
    jQuery('#crop_' + name).html('Image has changed or is empty. Please save and try again.');
    return;
  }
  var html = '<div class="cropper_modal" id="cropper_' + ts + '" style="float: left; padding: 10px 0 0 10px;">\
<img src="' + img + '" alt="" class="orig" style="max-width: 810px; max-height: 520px; display: block;"/>\
<br/>\
<input type="button" name="cancel" value="Cancel" onclick="cancel_cropper()"/> \
<input type="button" name="done" value="Set Crop" onclick="set_crop(\'' + name + '\')"/>\
</div>\
<div style="width:' + pw + 'px;height:' + ph + 'px;overflow:hidden; margin: 25px 0 0 5px; float: left;"><img src="' + img + '" class="crop_preview" alt="Preview" style=""></div>';
  
  jQuery(html).modal({containerCss: {width: 960, height: 600}});
  
  jQuery('#cropper_' + ts + ' img.orig').Jcrop(
    {
      aspectRatio: aspect,
      onChange: updatePreview,
      onSelect: updatePreview,
    }, function(){ jcrop_api = this; });
}

function updatePreview (c) {
  if (parseInt(c.w) > 0) {
    var rx = pw / c.w;
    var ry = ph / c.h;
    
    var bounds = jcrop_api.getBounds();
    var boundx = bounds[0];
    var boundy = bounds[1];
    
    $('.crop_preview').css({
      width: Math.round(rx * boundx) + 'px',
      height: Math.round(ry * boundy) + 'px',
      marginLeft: '-' + Math.round(rx * c.x) + 'px',
      marginTop: '-' + Math.round(ry * c.y) + 'px'
    });
  }
}

function cancel_cropper () {
  jQuery.modal.close();
}

function set_crop (name) {
  var c = jcrop_api.tellSelect();
  var imgh = jQuery('.jcrop-holder img').height();
  var imgw = jQuery('.jcrop-holder img').width();
  
  jQuery('#display_crop_' + name).html(' - Crop Set on Save: Width=' + c.w + ' Height=' + c.h + ', Start=' + c.x + ',' + c.y);
  jQuery('#id_crop_' + name).val(c.x + ',' + c.y + ',' + c.x2 + ',' + c.y2 + ',' + imgw + ',' + imgh);
  
  jQuery.modal.close();
}
