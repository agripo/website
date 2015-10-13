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

function show_then_hide(element){
    element.fadeIn();
    window.setTimeout(function(){element.fadeOut();}, 5000);
}


/* Shop add to cart */
call_after_dom_is_loaded(function($){
    function update_cart(run_after){
        var cart = $('#cart_contents');
        cart.empty();
        cart.append("Chargement du panier en cours")
        if(cart.length) {
            $.get(URL_GET_CART, function (ret) {
                // We empty the cart
                cart.empty();
                if(ret.total > 0){
                    $('.empty_cart').hide();
                    for(var product_id in ret.products){
                        var prod = ret.products[product_id];
                        var li = $('#cart_contents_model').html();
                        var properties = ['id', 'name', "quantity", "price"];
                        for(var property_id in properties){
                            var prop = properties[property_id];
                            li = li.replace(prop.toUpperCase(), prod[prop]);
                        }
                        cart.append(li);
                    }
                    $('#cart_module_total span').html(ret.total);
                    $('.not_empty_cart').show();
                    if(run_after){
                        run_after();
                    }
                }else{
                    $('.empty_cart').show();
                    $('.not_empty_cart').hide();
                }
            });
        }else{
            return false;
        }
    }

    update_cart();

    $("form.add_to_cart").submit(function(ev){
        form = ev.target.closest("form");
        id = $(form).find('input[name="id"]').val();
        quantity = $(form).find('input[name="quantity"]').val();
        $(form).find(".add_to_cart_please_wait_message").show();

        url = URL_ADD_TO_CART.replace('111111', id).replace('222222', quantity);
        $.get(url, function(ret){
            if(ret.error != undefined){
                $(form).find(".add_to_cart_please_wait_message").hide();
                if(ret.error == 'NO_STOCK'){
                    show_then_hide($(form).find('.add_to_cart_no_stock_message'));
                }else if(ret.error == "NOT_ENOUGH_STOCK") {
                    el = $(form).find('.add_to_cart_not_enough_stock_message');
                    show_then_hide(el);
                    el.html(el.html().replace("QUANTITY", ret.max));
                }
            }else{
                update_cart(function(){
                    window.setTimeout(
                        function() {
                            $(form).find(".add_to_cart_please_wait_message").hide();
                            show_then_hide($(form).find('.add_to_cart_confirm_message'));
                        },
                        500
                    );
                });
            }
        }, "json");

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
