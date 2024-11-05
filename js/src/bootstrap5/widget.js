import $ from 'jquery';
import {DictBase} from '../dict.js';

export class DictWidget extends DictBase {

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
        row +=         '<span class="bi-plus-circle-fill"> </span>';
        row +=       '</a>';
        row +=       '<a class="dict_row_remove" href="#">';
        row +=         '<span class="bi-dash-circle-fill"> </span>';
        row +=       '</a>';
        row +=       '<a class="dict_row_up" href="#">';
        row +=         '<span class="bi-arrow-up-circle-fill"> </span>';
        row +=       '</a>';
        row +=       '<a class="dict_row_down" href="#">';
        row +=         '<span class="bi-arrow-down-circle-fill"> </span>';
        row +=       '</a>';
        row +=     '</div>';
        row +=   '</td>';
        row += '</tr>';
        return $(row);
    }

    on_row_moved(row) {
        row.addClass('row-moved');
        setTimeout(function() {
            row.removeClass('row-moved');
        }, 1000);
    }

    add_first_handle(evt) {
        let row = super.add_first_handle(evt);
        this.on_row_moved(row);
    }

    add_handle(evt) {
        super.add_handle(evt);
        let action = evt.currentTarget,
            row = this.get_row(action);
        this.on_row_moved(row.next());
    }

    up_handle(evt) {
        evt.preventDefault();
        let row = this.get_row(evt.currentTarget);
        row.insertBefore(row.prev());
        this.reset_indices(row.parent());
        this.on_row_moved(row);
    }

    down_handle(evt) {
        evt.preventDefault();
        let row = this.get_row(evt.currentTarget);
        row.insertAfter(row.next());
        this.reset_indices(row.parent());
        this.on_row_moved(row);
    }
}

//////////////////////////////////////////////////////////////////////////////
// yafowil.widget.array integration
//////////////////////////////////////////////////////////////////////////////

function dict_on_array_add(inst, context) {
    DictWidget.initialize(context);
}

export function register_array_subscribers() {
    if (window.yafowil_array !== undefined) {
        window.yafowil_array.on_array_event('on_add', dict_on_array_add);
    } else if (yafowil.array !== undefined) {
        $.extend(yafowil.array.hooks.add, {
            dictwidget_binder: DictWidget.initialize
        });
    }
}
