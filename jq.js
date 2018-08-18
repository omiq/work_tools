


function load_gallery() {
    var url = 'http://geekahol.com/wp-json/wp/v2/posts?_embed';
    jQuery.getJSON( url, function( data ) {
    console.log(Date.now());
    jQuery(".image_gal").empty();
    data.forEach(function(item) {

        console.log(item);
        var src_img = item['_embedded']['wp:featuredmedia'][0]['media_details']['sizes']['medium_large']['source_url'];
        console.log(src_img);
        jQuery(".image_gal").append( "<img src='" + src_img + "'>" );
    })
});}



function timeout() {
    setTimeout(function () {
        load_gallery();
        timeout();
    }, 10000);
}

jQuery(document).ready(function () {
	load_gallery();
	timeout();
});


