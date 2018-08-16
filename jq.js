

jQuery(document).ready(function ($) {
	var url = 'http://geekahol.com/wp-json/wp/v2/posts?_embed';

	jQuery.getJSON( url, function( data ) {

		data.forEach(function(item) {
  console.log(item);
			var src_img = item['_embedded']['wp:featuredmedia'][0]['media_details']['sizes']['medium_large']['source_url'];
console.log(src_img);
  			$(".image_gal").append( "<img src='" + src_img + "'>" );
		})
	});
});


