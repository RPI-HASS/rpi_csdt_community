 $(function() {
    $('.row').each(function() {
        var intHeight = 0;
        $(this).find('.well').each(function() {
            if ($(this).outerHeight() > intHeight) {
                intHeight = $(this).outerHeight()
            }
        });
        console.log(intHeight);
        $(this).find('.well').each(function() {
            $(this).outerHeight(intHeight)
        });
    });
});