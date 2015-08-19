
(function ($) {
    $(document).ready(function(){
        $('#id_icon').hide();
        icon = $('#id_icon option:selected').html().substring(5);
        active = $('<div id="active_icon"><i title="'+icon+'" class="fa fa-' + icon + '"></i></div>');
        $('#id_icon').after(active);
        selector = $('<div id="icon_selector"><h1>Select the icon</h1></div>');
        options = $('#id_icon option');
        for(opt in options) {
            if(options[opt].innerHTML != undefined) {
                icon = options[opt].innerHTML.substring(5);
                selector.append('<i title="'+icon+'" class="fa fa-' + icon + '"></i>');
            }
        }
        $('body').prepend(selector);

        $('#active_icon').click(function(){
            $('#icon_selector').show();
        });

        $('#icon_selector i').click(function(ev){
            icon = ev.target.title;
            $('#icon_selector').hide();
            $('#active_icon i').attr('class', "fa fa-"+icon);
            $('#active_icon i').attr('title', icon);
            $('#id_icon option').val()
            val = $('#id_icon option').filter(
                function () {
                    return $(this).html() == "Icon "+icon;
                }
            ).val();
            $('#id_icon').val(val);
        });
    });
}(django.jQuery));

