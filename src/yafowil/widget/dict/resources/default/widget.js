var yafowil_dict = (function (exports, $) {
    'use strict';

    class DictBase {
        constructor(elem) {
            elem.data('yafowil-dict', this);
            this.elem = elem;
            let head_actions = $('> thead .dict_actions', elem),
                add_handle = this.add_first_handle.bind(this);
            $('a.dict_row_add', head_actions).off().on('click', add_handle);
            this.bind_actions();
        }
        bind_actions() {
            let actions_sel = '> tbody > tr > td.actions .dict_actions',
                row_actions = $(actions_sel, this.elem),
                add_handle = this.add_handle.bind(this),
                remove_handle = this.remove_handle.bind(this),
                up_handle = this.up_handle.bind(this),
                down_handle = this.down_handle.bind(this);
            this.mark_disabled(row_actions);
            $('a.dict_row_add', row_actions).off().on('click', add_handle);
            $('a.dict_row_remove', row_actions).off().on('click', remove_handle);
            $('a.dict_row_up', row_actions).off().on('click', up_handle);
            $('a.dict_row_down', row_actions).off().on('click', down_handle);
        }
        mark_disabled(row_actions) {
            $('a.dict_row_up', row_actions)
                .removeClass('dict_row_up_disabled')
                .first()
                .addClass('dict_row_up_disabled');
            $('a.dict_row_down', row_actions)
                .removeClass('dict_row_down_disabled')
                .last()
                .addClass('dict_row_down_disabled');
        }
        row_class(trigger, name) {
            for (let css of this.elem.attr('class').split(' ')) {
                if (css.substring(0, name.length) == name) {
                    return css.substring(name.length + 1, css.length);
                }
            }
            return '';
        }
        create_row(action) {
        }
        get_row(action) {
            return $(action).parent().parent().parent();
        }
        get base_name() {
            let id = this.elem.attr('id');
            return id.substring(11, id.length);
        }
        reset_indices(context) {
            var index = 0,
                base_name = this.base_name,
                base_id = base_name.replace(/\./g, '-');
            $('tr', context).each(function() {
                let row = $(this),
                    key = $('td.key input', row),
                    key_id = base_id + index + '-key',
                    key_name = base_name + index + '.key';
                key.attr('id', key_id).attr('name', key_name);
                let value = $('td.value input', row),
                    value_id = base_id + index + '-value',
                    value_name = base_name + index + '.value';
                value.attr('id', value_id).attr('name', value_name);
                index++;
            });
            this.bind_actions();
        }
        add_first_handle(evt) {
            evt.preventDefault();
            let new_row = this.create_row(evt.currentTarget),
                container = $('> tbody', this.elem);
            container.prepend(new_row);
            this.reset_indices(container);
        }
        add_handle(evt) {
            evt.preventDefault();
            let action = evt.currentTarget,
                row = this.get_row(action),
                new_row = this.create_row(action),
                container = row.parent();
            row.after(new_row);
            this.reset_indices(container);
        }
        remove_handle(evt) {
            evt.preventDefault();
            let row = this.get_row(evt.currentTarget);
            let container = row.parent();
            row.remove();
            this.reset_indices(container);
        }
        up_handle(evt) {
            evt.preventDefault();
            let row = this.get_row(evt.currentTarget);
            row.insertBefore(row.prev());
            this.reset_indices(row.parent());
        }
        down_handle(evt) {
            evt.preventDefault();
            let row = this.get_row(evt.currentTarget);
            row.insertAfter(row.next());
            this.reset_indices(row.parent());
        }
    }

    class DictWidget extends DictBase {
        static initialize(context) {
            $('table.dictwidget', context).each(function() {
                let elem = $(this);
                if (window.yafowil_array !== undefined &&
                    window.yafowil_array.inside_template(elem)) {
                    return;
                }
                new DictWidget(elem);
            });
        }
        create_row(action) {
            let key_css = this.row_class(action, 'key'),
                val_css = this.row_class(action, 'value'),
                row = '';
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
        }
    }
    function dict_on_array_add(inst, context) {
        DictWidget.initialize(context);
    }
    function register_array_subscribers() {
        if (window.yafowil_array !== undefined) {
            window.yafowil_array.on_array_event('on_add', dict_on_array_add);
        } else if (yafowil.array !== undefined) {
            $.extend(yafowil.array.hooks.add, {
                dictwidget_binder: DictWidget.initialize
            });
        }
    }

    $(function() {
        if (window.ts !== undefined) {
            ts.ajax.register(DictWidget.initialize, true);
        } else if (window.bdajax !== undefined) {
            bdajax.register(DictWidget.initialize, true);
        } else {
            DictWidget.initialize();
        }
        register_array_subscribers();
    });

    exports.DictWidget = DictWidget;
    exports.register_array_subscribers = register_array_subscribers;

    Object.defineProperty(exports, '__esModule', { value: true });


    window.yafowil = window.yafowil || {};
    window.yafowil.dict = exports;


    return exports;

})({}, jQuery);
