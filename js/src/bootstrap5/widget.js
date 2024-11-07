import $ from 'jquery';
import {DictBase} from '../base/dict.js';

export class DictWidget extends DictBase {

    /**
     * Initializes each widget in the given DOM context.
     * 
     * @param {jQuery} context - DOM context for initialization.
     */
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

    /**
     * Creates a new row for the dictionary widget with input fields for key
     * and value, as well as action buttons for managing the row.
     * @param {string} action - The action type for styling the row.
     * @returns {jQuery} - A jQuery object representing the new row.
     */
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

    /**
     * Marks a row as moved by adding a CSS class and removing it after a timeout.
     * @param {jQuery} row - The row element that has been moved.
     */
    highlight(row) {
        row.addClass('row-moved');
        setTimeout(function() {
            row.removeClass('row-moved');
        }, 1000);
    }

    /**
     * Handles the event when the first row is added.
     * @param {Event} evt - The event object triggered by the addition.
     * @returns {jQuery} - The newly added row element.
     */
    add_first_handle(evt) {
        let row = super.add_first_handle(evt);
        this.highlight(row);
        return row;
    }

    /**
     * Handles the event when a new row is added.
     * @param {Event} evt - The event object triggered by the addition.
     */
    add_handle(evt) {
        super.add_handle(evt);
        let action = evt.currentTarget,
            row = this.get_row(action);
        this.highlight(row.next());
    }

    /**
     * Moves the selected row up in the table.
     * @param {Event} evt - The event object triggered by the up action.
     */
    up_handle(evt) {
        evt.preventDefault();
        let row = this.get_row(evt.currentTarget);
        row.insertBefore(row.prev());
        this.reset_indices(row.parent());
        this.highlight(row);
    }

    /**
     * Moves the selected row down in the table.
     * @param {Event} evt - The event object triggered by the down action.
     */
    down_handle(evt) {
        evt.preventDefault();
        let row = this.get_row(evt.currentTarget);
        row.insertAfter(row.next());
        this.reset_indices(row.parent());
        this.highlight(row);
    }
}

//////////////////////////////////////////////////////////////////////////////
// yafowil.widget.array integration
//////////////////////////////////////////////////////////////////////////////

/**
 * Re-initializes widget on array add event.
 */
function dict_on_array_add(inst, context) {
    DictWidget.initialize(context);
}

/**
 * Registers subscribers to yafowil array events.
 */
export function register_array_subscribers() {
    if (window.yafowil_array !== undefined) {
        window.yafowil_array.on_array_event('on_add', dict_on_array_add);
    } else if (yafowil.array !== undefined) {
        $.extend(yafowil.array.hooks.add, {
            dictwidget_binder: DictWidget.initialize
        });
    }
}
