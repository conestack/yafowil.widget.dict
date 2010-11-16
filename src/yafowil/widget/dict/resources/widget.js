if (typeof(window['yafowil']) == "undefined") yafowil = {};

(function($) {

    $(document).ready(function() {
        yafowil.dictwidget.binder();
        bdajax.binders.dictwidget_binder = yafowil.dictwidget.binder;
    });
    
    // yafowil dictwidget
    $.extend(yafowil, {
        
        dictwidget: {
            
            base_id: 'input-editform-users_attrmap-entry',
            
            base_name: 'editform.users_attrmap.entry',
            
            create_row: function() {
                var row = '';
                row += '<tr>';
                row +=   '<td class="key">';
                row +=     '<input type="text" value="" />';
                row +=   '</td>';
                row +=   '<td class="value">';
                row +=     '<input type="text" value="" />';
                row +=   '</td>';
                row +=   '<td>';
                row +=     '<div class="dict_actions">';
                row +=       '<a class="dict_row_add" href="#">&nbsp;</a>';
                row +=       '<a class="dict_row_remove" href="#">&nbsp</a>';
                row +=       '<a class="dict_row_up" href="#">&nbsp</a>';
                row +=       '<a class="dict_row_down" href="#">&nbsp</a>';
                row +=     '</div>';
                row +=   '</td>';
                row += '</tr>';
                return row;
            },
            
            get_row: function(action) {
                return $(action).parent().parent().parent();
            },
            
            reset_indices: function(context) {
                var index = 0;
                $('tr', context).each(function() {
                    row = $(this);
                    key = $('td.key input', row);
                    key_id = yafowil.dictwidget.base_id + index + '-key';
                    key_name = yafowil.dictwidget.base_name + index + '.key';
                    key.attr('id', key_id).attr('name', key_name);
                    value = $('td.value input', row);
                    value_id = yafowil.dictwidget.base_id + index + '-value';
                    value_name = yafowil.dictwidget.base_name + index + '.value';
                    value.attr('id', value_id).attr('name', value_name);
                    index++;
                });
                yafowil.dictwidget.binder(context);
                yafowil.dictwidget.mark_disabled(context);
            },
            
            mark_disabled: function(context) {
                $('a.dict_row_up', context)
                    .removeClass('dict_row_up_disabled');
                $('a.dict_row_up', context)
                    .first()
                    .addClass('dict_row_up_disabled');
                $('a.dict_row_down', context)
                    .removeClass('dict_row_down_disabled');
                $('a.dict_row_down', context)
                    .last()
                    .addClass('dict_row_down_disabled');
            },
            
            binder: function(context) {
                yafowil.dictwidget.mark_disabled(context);
                $('a.dict_row_add', context)
                    .unbind()
                    .bind('click', function(event) {
                        event.preventDefault();
                        var row = yafowil.dictwidget.get_row(this);
                        var new_row = yafowil.dictwidget.create_row();
                        var container = row.parent();
                        if (container.get(0).tagName.toLowerCase() == 'tbody') {
                            row.after(new_row);
                        } else {
                            container = $('tbody', container.parent());
                            container.prepend(new_row);
                        }
                        yafowil.dictwidget.reset_indices(container);
                    });
                
                $('a.dict_row_remove', context)
                    .unbind()
                    .bind('click', function(event) {
                        event.preventDefault();
                        var row = yafowil.dictwidget.get_row(this);
                        row.remove();
                        yafowil.dictwidget.reset_indices(row.parent());
                    });
                
                $('a.dict_row_up', context)
                    .unbind()
                    .bind('click', function(event) {
                        event.preventDefault();
                        var row = yafowil.dictwidget.get_row(this);
                        row.insertBefore(row.prev());
                        yafowil.dictwidget.reset_indices(row.parent());
                    });
                
                $('a.dict_row_down', context)
                    .unbind()
                    .bind('click', function(event) {
                        event.preventDefault();
                        var row = yafowil.dictwidget.get_row(this);
                        row.insertAfter(row.next());
                        yafowil.dictwidget.reset_indices(row.parent());
                    });
            }
        }
    });

})(jQuery);