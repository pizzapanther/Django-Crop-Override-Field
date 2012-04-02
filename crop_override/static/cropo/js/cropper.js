var jcrop_api;

function show_cropper (name, orig, aspect) {
  var d = new Date();
  var ts = d.getTime();
  
  var img = jQuery('#id_orig_' + orig).val();
  var html = '<div class="cropper_modal" id="cropper_' + ts + '" style="width: 940px; margin: 0 auto;">\
<img src="' + img + '" alt="" style="max-width: 940px; max-height: 520px; display: block; margin: 0 auto;"/>\
<br/>\
<input type="button" name="cancel" value="Cancel" onclick="cancel_cropper()"/> \
<input type="button" name="done" value="Set Crop" onclick="set_crop(\'' + name + '\')"/>\
</div>';
  
  jQuery(html).modal({containerCss: {width: 960, height: 600}});
  
  jQuery('#cropper_' + ts + ' img').Jcrop({aspectRatio: aspect}, function(){ jcrop_api = this; });
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