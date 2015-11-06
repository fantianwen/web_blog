/**
 * Created by RadAsm on 15/11/6.
 */
$(document).ready(function () {
    var logo = $('.logo');
    logo.hover(function () {
        $(this).css('color', '#FF7F50');
    }).mouseleave(function () {
        $(this).css('color', '#000');
    });

    var title = $('.title');
    title.hover(function () {
        $('#title').css('text_decoration', 'underline');
    }).mouseleave(function () {
        $('#title').css('text_decoration', 'none');
    });
})