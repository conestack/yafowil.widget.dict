import { DictWidget } from "../src/widget";

QUnit.test('test', assert => {
    let el = $('<table />').addClass('dictwidget').appendTo('body');
    DictWidget.initialize();
    let widget = el.data('yafowil-dict');
    assert.ok(widget);

    el.remove();
    widget = null;
});