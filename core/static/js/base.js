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

/* news module rotation */
call_after_dom_is_loaded(function($){
    active_news = 0;
    loop_around_the_news = true
    news = $('input[name="shown_news"]');
    next_news = function(){
        if(loop_around_the_news) {
            active_news += 1;
            if(active_news > 2){
                active_news = 0;
            }
            news[active_news].checked = true;
            window.setTimeout(next_news, NEWS_MODULE_ROTATION_DELAY);
        }
    };

    window.setTimeout(next_news, NEWS_MODULE_ROTATION_DELAY);
    $('.one_news_selector').click(function(){
        loop_around_the_news = false;
    })
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
