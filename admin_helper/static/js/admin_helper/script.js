document.addEventListener('DOMContentLoaded', function() {
    var manage_field = function(found_field, field){
        found_field.click(function(ev){
            var old_content = $(ev.target).html();
            var the_field = field;
            var td = ev.target;
            var entry_id = $(td).parents('tr').find(".action-select").val();
            var type = the_field['type'];
            if(type == "IntegerField" || type == "CharField") {
                var regex = /[^<]*/;
                var field_content = '<input style="width:90%;" value="' + old_content + '" type="text"/>&nbsp;';
                var view = 'set_text';
                if(type == "IntegerField"){
                    regex = /^[0-9]+$/;
                    field_content = '<input min="'+field['min']+'" max="'+field['max']+'" value="' + old_content + '" style="width:50px" type="number"/>&nbsp;';
                    view = 'set_number';
                }
                if(old_content.match(regex)){
                    var yes_image = $('<img src="/static/admin/img/icon-yes.gif"/>');
                    $(td).html(field_content);
                    $(td).append(yes_image);
                    yes_image.click(function (ev2) {
                        ev2.stopImmediatePropagation();
                        var val = $(td).find("input").val()
                        var url = entry_id.toString() + '/'+the_field['name']+'/'+view+'/?value='+val;
                        document.location = url;
                    })
                }
            }else if(type == 'BooleanField'){
                var url = entry_id.toString() + '/'+the_field['name']+'/set_on_off/';
                document.location = url;
            }
        }).css('cursor', 'pointer');
    }

    // We get the models structure for this admin page
    if($("#changelist").length) {
        $.get('admin_helper_model_structure/', function (ret) {
            for (var id in ret.fields) {
                var field = ret.fields[id];
                $('.column-' + field['name']).addClass('admin-helper-editable-column');
                manage_field($(".field-" + field['name']), field);
            }
        });
    }
}, false);
