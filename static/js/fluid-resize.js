// Find all YouTube videos
//var $allVideos = $("iframe[src^='http://www.youtube.com']"),
var $allVideos = $("iframe"),

    // The element that is fluid width
    $fluidEl = $("body");

// Figure out and save aspect ratio for each video
$allVideos.each(function() {

  $(this)
    .data('aspectRatio', this.height / this.width)

    // and remove the hard coded width/height
    .removeAttr('height')
    .removeAttr('width');

});

var __bnm = "";

console.log("Here");

$('body').keypress(function(event) {
    console.log("Have key "+event.key);
    if(event.key == "Right")
        __bnm += "r";
    else if (event.key == "Left")
        __bnm += "l";
    else if (event.key == "Up")
        __bnm += "u";
    else if (event.key == "Down")
        __bnm += "d";
    else if (event.key == "a")
        __bnm += "a";
    else if (event.key == "b")
        __bnm += "b";
    else if (event.key == "Enter")
        __bnm += "e";
    else
        __bnm = "";

    if(__bnm == "uuddlrlrbae") {
        __bnm = "";
        console.log("Show the kitty cat!");
        $('body').append('<img class="__bnm" src="/static/js/create/animate.gif" style="position: absolute; left: 33%; top: 33%; z-index=100;">');
        window.setTimeout(function() {
            $('.__bnm').remove();
        }, 5000);
    }
});
