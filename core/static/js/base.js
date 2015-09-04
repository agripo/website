/*
 * CAUTION : DO NOT USE JQUERY OUTSIDE OF THE FUNCTIONS GIVEN AS CALLBACK TO
 * call_after_dom_is_loaded(callback)
**/

/* Settings */
NEWS_MODULE_ROTATION_DELAY = 10000;

/* Shared functions */
var _func_to_call_after_dom_is_loaded = [];
function call_after_dom_is_loaded(callback){
    _func_to_call_after_dom_is_loaded.push(callback);
}
function dom_is_loaded($){
    for(callback in _func_to_call_after_dom_is_loaded){
        func = _func_to_call_after_dom_is_loaded[callback];
        func($);
    }
}

/* Shop add to cart */
call_after_dom_is_loaded(function(){
    $("form.add_to_cart").submit(function(ev){
        form = ev.target.closest("form");
        id = $(form).find('input[name="id"]').val();
        quantity = $(form).find('input[name="quantity"]').val();

        $.GET('')

        $(form).find('.add_to_cart_confirm_message').fadeIn();
        window.setTimeout(function(){
            $(form).find('.add_to_cart_confirm_message').fadeOut();
        }, 5000);
        return false;
    });
});

/* Cookies notification */
call_after_dom_is_loaded(function($){
    $('#id_uses_cookies').click(function(){
        $.get(
                URL_COOKIES_ACCEPTED,
                function(){
                    $('#id_uses_cookies_section').hide();
                }
        );
        return false;
    });
});
