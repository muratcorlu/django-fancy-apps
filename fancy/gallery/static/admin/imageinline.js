(function($){
    $('.field-image .file-upload').each(function(i, elem) {
        var imageUrl = $(elem).find('a').attr('href');
        $(elem).append( $('<img src="'+ imageUrl +'" height="100" />');
    });
})(django.jQuery);