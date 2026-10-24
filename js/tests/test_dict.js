import $ from 'jquery';
import { DictBase } from '../src/base/dict.js';
import { DictWidget, register_array_subscribers } from '../src/default/widget.js';

const all_actions =
    '<a class="dict_row_add" href="#"><span class="icon-plus-sign"> </span></a>' +
    '<a class="dict_row_remove" href="#"><span class="icon-minus-sign"> </span></a>' +
    '<a class="dict_row_up" href="#"><span class="icon-circle-arrow-up"> </span></a>' +
    '<a class="dict_row_down" href="#"><span class="icon-circle-arrow-down"> </span></a>';

function create_dict(entries) {
    let body = '';
    for (let i = 0; i < entries; i++) {
        body += `
            <tr>
              <td class="key">
                <input class="keyfield" id="input-mydict-entry${i}-key"
                       name="mydict.entry${i}.key" type="text" value="key${i}" />
              </td>
              <td class="value">
                <input class="valuefield" id="input-mydict-entry${i}-value"
                       name="mydict.entry${i}.value" type="text" value="value${i}" />
              </td>
              <td class="actions">
                <div class="dict_actions">${all_actions}</div>
              </td>
            </tr>`;
    }
    return $(`
        <table class="dictwidget key-keyfield value-valuefield" id="dictwidget_mydict.entry">
          <thead>
            <tr>
              <th>Key</th>
              <th>Value</th>
              <th class="actions">
                <div class="dict_actions">
                  <a class="dict_row_add" href="#"><span class="icon-plus-sign"> </span></a>
                </div>
              </th>
            </tr>
          </thead>
          <tbody>${body}</tbody>
        </table>`).appendTo('body');
}

function rows(elem) {
    return $('> tbody > tr', elem);
}

function row_keys(elem) {
    return rows(elem)
        .map((_, row) => $('td.key input', row).val())
        .get();
}

function assert_names(assert, elem) {
    rows(elem).each((index, row) => {
        assert.strictEqual($('td.key input', row).attr('name'), `mydict.entry${index}.key`);
        assert.strictEqual($('td.value input', row).attr('name'), `mydict.entry${index}.value`);
    });
}

function click(elem) {
    const evt = $.Event('click');
    elem.trigger(evt);
    return evt;
}

QUnit.test('test', (assert) => {
    const el = $('<table />').addClass('dictwidget').appendTo('body');
    DictWidget.initialize();
    let widget = el.data('yafowil-dict');
    assert.ok(widget);

    el.remove();
    widget = null;
});

QUnit.test('register_array_subscribers', (assert) => {
    const _array_subscribers = {
        on_add: [],
    };

    // patch window.yafowil
    window.yafowil = {
        array: undefined,
    };

    // return if window.yafowil === undefined
    register_array_subscribers();
    assert.deepEqual(_array_subscribers.on_add, []);

    // patch yafowil_array
    window.yafowil_array = {
        on_array_event: (evt_name, evt_function) => {
            _array_subscribers[evt_name] = evt_function;
        },
        inside_template(elem) {
            return elem.parents('.arraytemplate').length > 0;
        },
    };
    register_array_subscribers();

    // create table DOM
    const table = $('<table />').append($('<tr id="row" />')).append($('<td />')).appendTo('body');
    $('td', table).addClass('arraytemplate');

    const el = $('<table />').addClass('dictwidget');
    el.appendTo($('td', table));

    // invoke array on_add - returns
    const context = $('#row');
    _array_subscribers.on_add.apply(null, context);
    let widget = el.data('yafowil-dict');
    assert.notOk(widget);
    $('td', table).removeClass('arraytemplate');

    // invoke array on_add
    _array_subscribers.on_add.apply(null, context);
    widget = el.data('yafowil-dict');
    assert.ok(widget);

    table.remove();
    window.yafowil_array = undefined;
    window.yafowil = undefined;
    widget = null;
});

QUnit.test('register_array_subscribers with legacy array hooks', (assert) => {
    window.yafowil = {
        array: {
            hooks: {
                add: {},
            },
        },
    };
    register_array_subscribers();
    assert.strictEqual(window.yafowil.array.hooks.add.dictwidget_binder, DictWidget.initialize);
    window.yafowil = undefined;
});

QUnit.module('DictWidget', (hooks) => {
    let elem;

    hooks.afterEach(() => {
        elem.remove();
    });

    QUnit.test('initialize respects context', (assert) => {
        elem = create_dict(0);
        DictWidget.initialize($('<div />'));
        assert.strictEqual(elem.data('yafowil-dict'), undefined);
        DictWidget.initialize(elem.parent());
        assert.true(elem.data('yafowil-dict') instanceof DictWidget);
    });

    QUnit.test('constructor', (assert) => {
        elem = create_dict(0);
        const wid = new DictWidget(elem);
        assert.true(wid instanceof DictBase);
        assert.strictEqual(elem.data('yafowil-dict'), wid);
        assert.true(wid.elem.is(elem));
        assert.strictEqual(wid.base_name, 'mydict.entry');
    });

    QUnit.test('row_class', (assert) => {
        elem = create_dict(0);
        const wid = new DictWidget(elem);
        assert.strictEqual(wid.row_class(null, 'key'), 'keyfield');
        assert.strictEqual(wid.row_class(null, 'value'), 'valuefield');
        assert.strictEqual(wid.row_class(null, 'other'), '');
    });

    QUnit.test('create_row', (assert) => {
        elem = create_dict(0);
        const wid = new DictWidget(elem);
        const row = $(wid.create_row());
        assert.true(row.is('tr'));
        assert.true($('td.key input', row).hasClass('keyfield'));
        assert.strictEqual($('td.key input', row).val(), '');
        assert.true($('td.value input', row).hasClass('valuefield'));
        assert.strictEqual($('td.value input', row).val(), '');
        const actions = $('td.actions .dict_actions a', row);
        assert.deepEqual(actions.map((_, el) => el.className).get(), [
            'dict_row_add',
            'dict_row_remove',
            'dict_row_up',
            'dict_row_down',
        ]);
        assert.deepEqual(
            $('span', actions)
                .map((_, el) => el.className)
                .get(),
            ['icon-plus-sign', 'icon-minus-sign', 'icon-circle-arrow-up', 'icon-circle-arrow-down'],
        );
    });

    QUnit.test('mark disabled', (assert) => {
        elem = create_dict(3);
        new DictWidget(elem);
        assert.deepEqual(
            $('a.dict_row_up', elem)
                .map((_, el) => $(el).hasClass('dict_row_up_disabled'))
                .get(),
            [true, false, false],
        );
        assert.deepEqual(
            $('a.dict_row_down', elem)
                .map((_, el) => $(el).hasClass('dict_row_down_disabled'))
                .get(),
            [false, false, true],
        );
    });

    QUnit.test('add first row', (assert) => {
        elem = create_dict(2);
        new DictWidget(elem);
        const evt = click($('> thead a.dict_row_add', elem));
        assert.true(evt.isDefaultPrevented());
        assert.deepEqual(row_keys(elem), ['', 'key0', 'key1']);
        assert_names(assert, elem);

        // actions of new row are bound
        click($('a.dict_row_remove', rows(elem).first()));
        assert.deepEqual(row_keys(elem), ['key0', 'key1']);
    });

    QUnit.test('add row', (assert) => {
        elem = create_dict(2);
        new DictWidget(elem);
        const evt = click($('a.dict_row_add', rows(elem).first()));
        assert.true(evt.isDefaultPrevented());
        assert.deepEqual(row_keys(elem), ['key0', '', 'key1']);
        assert_names(assert, elem);
    });

    QUnit.test('remove row', (assert) => {
        elem = create_dict(3);
        new DictWidget(elem);
        const evt = click($('a.dict_row_remove', rows(elem).eq(1)));
        assert.true(evt.isDefaultPrevented());
        assert.deepEqual(row_keys(elem), ['key0', 'key2']);
        assert_names(assert, elem);
    });

    QUnit.test('move row up', (assert) => {
        elem = create_dict(3);
        new DictWidget(elem);
        const row = rows(elem).eq(2);
        const evt = click($('a.dict_row_up', row));
        assert.true(evt.isDefaultPrevented());
        assert.deepEqual(row_keys(elem), ['key0', 'key2', 'key1']);
        assert_names(assert, elem);
        assert.false($('a.dict_row_down', row).hasClass('dict_row_down_disabled'));
        assert.true($('a.dict_row_down', rows(elem).last()).hasClass('dict_row_down_disabled'));
    });

    QUnit.test('move row down', (assert) => {
        elem = create_dict(3);
        new DictWidget(elem);
        const row = rows(elem).eq(0);
        const evt = click($('a.dict_row_down', row));
        assert.true(evt.isDefaultPrevented());
        assert.deepEqual(row_keys(elem), ['key1', 'key0', 'key2']);
        assert_names(assert, elem);
        assert.false($('a.dict_row_up', row).hasClass('dict_row_up_disabled'));
        assert.true($('a.dict_row_up', rows(elem).first()).hasClass('dict_row_up_disabled'));
    });

    QUnit.test('DictBase.create_row is implemented by subclasses', (assert) => {
        elem = create_dict(0);
        const wid = new DictBase(elem);
        assert.strictEqual(wid.create_row(), undefined);
    });
});
