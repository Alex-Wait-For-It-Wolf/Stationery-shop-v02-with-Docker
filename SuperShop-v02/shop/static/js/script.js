$(function() {

        /* Menu nav toggle */
    $("#menu_toggle").on("click", function(event) {
        event.preventDefault();

        $(this).toggleClass("active");
        $("#menu").toggleClass("active");
    });

    $('.languages-btn').click(function() {
      $('.languages ul').fadeToggle(500);
    });
});
