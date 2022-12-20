import { DictWidget } from "../src/widget";
import {register_array_subscribers} from "../src/widget";

QUnit.test('test', assert => {
    let el = $('<table />').addClass('dictwidget').appendTo('body');
    DictWidget.initialize();
    let widget = el.data('yafowil-dict');
    assert.ok(widget);

    el.remove();
    widget = null;
});

QUnit.test('register_array_subscribers', assert => {
    let _array_subscribers = {
        on_add: []
    };

    // patch window.yafowil
    window.yafowil = {
        array: undefined
    }

    // return if window.yafowil === undefined
    register_array_subscribers();
    assert.deepEqual(_array_subscribers['on_add'], []);

    // patch yafowil_array
    window.yafowil_array = {
        on_array_event: function(evt_name, evt_function) {
            _array_subscribers[evt_name] = evt_function;
        }
    };
    register_array_subscribers();

    // create table DOM
    let table = $('<table />')
        .append($('<tr />'))
        .append($('<td />'))
        .appendTo('body');

    let el = $('<table />').addClass('dictwidget');
    el.appendTo($('td', table));

    // invoke array on_add
    _array_subscribers['on_add'].apply(null, $('tr', table));
    let widget = el.data('yafowil-dict');
    assert.ok(widget);

    table.remove();
    window.yafowil_array = undefined;
    window.yafowil = undefined;
    widget = null;
});
