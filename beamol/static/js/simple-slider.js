$(document).ready(function ($) {
    setInterval(function () {
        moveRight();
    }, 8000);

    $('#slider ul li:last-child').prependTo('#slider ul');

    function resizeSlider() {
        var slideWidth = $('#slider').width();
        var slideCount = $('#slider ul li').length;
        var sliderUlWidth = slideCount * slideWidth;

        $('#slider ul li').css({ width: slideWidth });
        $('#slider ul').css({ width: sliderUlWidth, marginLeft: - slideWidth });

        $.each($('.title-box'), function() {
            $(this).css({ 'line-height': $(this).height() + 'px' });
        });
    }

    resizeSlider();

    $(window).on("resize", function() {
        resizeSlider();
    } );

    function moveLeft() {
        var slideWidth = $('#slider').width();
        $('#slider ul').animate({
            left: + slideWidth
        }, 1000, function () {
            $('#slider ul li:last-child').prependTo('#slider ul');
            $('#slider ul').css('left', '');
        });
    };

    function moveRight() {
        var slideWidth = $('#slider').width();
        $('#slider ul').animate({
            left: - slideWidth
        }, 1000, function () {
            $('#slider ul li:first-child').appendTo('#slider ul');
            $('#slider ul').css('left', '');
        });
    };

    $('a.control_prev').click(function () {
        moveLeft();
    });

    $('a.control_next').click(function () {
        moveRight();
    });

});
