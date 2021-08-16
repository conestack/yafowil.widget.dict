/* 
 * yafowil dict widget
 * 
 * Requires: jquery
 * Optional: bdajax
 */

if (typeof(window['yafowil']) == "undefined") yafowil = {};

(function($) {

    $(document).ready(function() {
        // initial binding
        yafowil.dict.binder();

        // add after ajax binding if bdajax present
        if (typeof(window['bdajax']) != "undefined") {
            $.extend(bdajax.binders, {
                dictwidget_binder: yafowil.dict.binder
            });
        }

        // add binder to yafowil.widget.array hooks
        if (typeof(window.yafowil['array']) != "undefined") {
            $.extend(yafowil.array.hooks.add, {
                dictwidget_binder: yafowil.dict.binder
            });
        }
    });

    $.extend(yafowil, {

        dict: {

            create_row: function(key_css, val_css) {
                var row = '';
                row += '<tr>';
                row +=   '<td class="key">';
                row +=     '<input type="text" class="' + key_css + '" value="" />';
                row +=   '</td>';
                row +=   '<td class="value">';
                row +=     '<input type="text" class="' + val_css + '" value="" />';
                row +=   '</td>';
                row +=   '<td class="actions">';
                row +=     '<div class="dict_actions">';
                row +=       '<a class="dict_row_add" href="#">';
                row +=         '<span class="icon-plus-sign"> </span>';
                row +=       '</a>';
                row +=       '<a class="dict_row_remove" href="#">';
                row +=         '<span class="icon-minus-sign"> </span>';
                row +=       '</a>';
                row +=       '<a class="dict_row_up" href="#">';
                row +=         '<span class="icon-circle-arrow-up"> </span>';
                row +=       '</a>';
                row +=       '<a class="dict_row_down" href="#">';
                row +=         '<span class="icon-circle-arrow-down"> </span>';
                row +=       '</a>';
                row +=     '</div>';
                row +=   '</td>';
                row += '</tr>';
                return row;
            },

            get_row: function(action) {
                return $(action).parent().parent().parent();
            },

            base_name: function(context) {
                return context.parents('.dictwidget').attr('id');
            },

            reset_indices: function(context) {
                var index = 0;
                var base_name = yafowil.dict.base_name(context);
                base_name = base_name.substring(11, base_name.length);
                var base_id = base_name.replace(/\./g, '-');
                $('tr', context).each(function() {
                    row = $(this);
                    key = $('td.key input', row);
                    key_id = base_id + index + '-key';
                    key_name = base_name + index + '.key';
                    key.attr('id', key_id).attr('name', key_name);
                    value = $('td.value input', row);
                    value_id = base_id + index + '-value';
                    value_name = base_name + index + '.value';
                    value.attr('id', value_id).attr('name', value_name);
                    index++;
                });
                yafowil.dict.binder(context);
            },

            mark_disabled: function(context) {
                context = $(context);
                $('a.dict_row_up', context)
                    .removeClass('dict_row_up_disabled')
                    .first()
                    .addClass('dict_row_up_disabled');
                $('a.dict_row_down', context)
                    .removeClass('dict_row_down_disabled')
                    .last()
                    .addClass('dict_row_down_disabled');
            },

            add_class: function(trigger, name) {
                var table = $(trigger).closest('table');
                classes = table.attr('class').split(' ');
                var idx, css;
                for (idx in classes) {
                    css = classes[idx];
                    if (css.substring(0, name.length) == name) {
                        return css.substring(name.length + 1, css.length);
                    }
                }
                return '';
            },

            binder: function(context) {
                yafowil.dict.mark_disabled(context);
                $('a.dict_row_add', context)
                    .unbind()
                    .bind('click', function(event) {
                        event.preventDefault();
                        var key_css = yafowil.dict.add_class(this, 'key');
                        var val_css = yafowil.dict.add_class(this, 'value');
                        var row = yafowil.dict.get_row(this);
                        var new_row = yafowil.dict.create_row(key_css, val_css);
                        var container = row.parent();
                        if (container.get(0).tagName.toLowerCase() == 'tbody') {
                            row.after(new_row);
                        } else {
                            var table = container.parent();
                            var body = $('tbody', table);
                            container = body;
                            container.prepend(new_row);
                        }
                        yafowil.dict.reset_indices(container);
                    });

                $('a.dict_row_remove', context)
                    .unbind()
                    .bind('click', function(event) {
                        event.preventDefault();
                        var row = yafowil.dict.get_row(this);
                        var container = row.parent();
                        row.remove();
                        yafowil.dict.reset_indices(container);
                    });

                $('a.dict_row_up', context)
                    .unbind()
                    .bind('click', function(event) {
                        event.preventDefault();
                        var row = yafowil.dict.get_row(this);
                        row.insertBefore(row.prev());
                        yafowil.dict.reset_indices(row.parent());
                    });

                $('a.dict_row_down', context)
                    .unbind()
                    .bind('click', function(event) {
                        event.preventDefault();
                        var row = yafowil.dict.get_row(this);
                        row.insertAfter(row.next());
                        yafowil.dict.reset_indices(row.parent());
                    });
            }
        }
    });

})(jQuery);