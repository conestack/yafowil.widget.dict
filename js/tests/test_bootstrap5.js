import $ from 'jquery';
import { DictBase } from '../src/base/dict.js';
import { DictWidget, register_array_subscribers } from '../src/bootstrap5/widget.js';

function create_dict(entries) {
    let body = '';
    for (let i = 0; i < entries; i++) {
        body += `
            <tr>
              <td class="key"><input name="mydict.entry${i}.key" value="key${i}" /></td>
              <td class="value"><input name="mydict.entry${i}.value" value="value${i}" /></td>
              <td class="actions">
                <div class="dict_actions">
                  <a class="dict_row_add" href="#"></a>
                  <a class="dict_row_up" href="#"></a>
                  <a class="dict_row_down" href="#"></a>
                </div>
              </td>
            </tr>`;
    }
    return $(`
        <table class="dictwidget key-keyfield value-valuefield" id="dictwidget_mydict.entry">
          <thead>
            <tr>
              <th class="actions">
                <div class="dict_actions"><a class="dict_row_add" href="#"></a></div>
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

function assert_ids_and_names(assert, elem) {
    rows(elem).each((index, row) => {
        const key = $('td.key input', row),
            value = $('td.value input', row);
        assert.strictEqual(key.attr('id'), `input-mydict-entry${index}-key`);
        assert.strictEqual(key.attr('name'), `mydict.entry${index}.key`);
        assert.strictEqual(value.attr('id'), `input-mydict-entry${index}-value`);
        assert.strictEqual(value.attr('name'), `mydict.entry${index}.value`);
    });
}

function click(elem) {
    const evt = $.Event('click');
    elem.trigger(evt);
    return evt;
}

QUnit.module('bootstrap5 DictWidget', (hooks) => {
    const orig_set_timeout = window.setTimeout;
    let elem, timeouts;

    hooks.beforeEach(() => {
        timeouts = [];
        // run highlight timeouts on demand instead of waiting
        window.setTimeout = (fn, delay) => {
            timeouts.push([fn, delay]);
        };
    });
    hooks.afterEach(() => {
        window.setTimeout = orig_set_timeout;
        if (elem) {
            elem.remove();
            elem = null;
        }
        delete window.yafowil_array;
        delete window.yafowil;
    });

    function run_timeouts(assert) {
        for (const [fn, delay] of timeouts) {
            assert.strictEqual(delay, 1000);
            fn();
        }
        timeouts = [];
    }

    QUnit.test('initialize', (assert) => {
        elem = create_dict(0);
        DictWidget.initialize();
        const wid = elem.data('yafowil-dict');
        assert.true(wid instanceof DictWidget);
        assert.true(wid instanceof DictBase);
    });

    QUnit.test('create_row', (assert) => {
        elem = create_dict(0);
        const wid = new DictWidget(elem);
        const row = wid.create_row();
        assert.true(row instanceof $);
        assert.true(row.is('tr'));
        assert.true($('td.key input', row).hasClass('keyfield'));
        assert.true($('td.value input', row).hasClass('valuefield'));
        assert.deepEqual(
            $('td.actions .dict_actions a', row)
                .map((_, el) => el.className)
                .get(),
            ['dict_row_add', 'dict_row_remove', 'dict_row_up', 'dict_row_down'],
        );
        assert.deepEqual(
            $('td.actions span', row)
                .map((_, el) => el.className)
                .get(),
            [
                'bi-plus-circle-fill',
                'bi-dash-circle-fill',
                'bi-arrow-up-circle-fill',
                'bi-arrow-down-circle-fill',
            ],
        );
    });

    QUnit.test('add first row highlights new row', (assert) => {
        elem = create_dict(1);
        new DictWidget(elem);
        const evt = click($('> thead a.dict_row_add', elem));
        assert.true(evt.isDefaultPrevented());
        assert.deepEqual(row_keys(elem), ['', 'key0']);
        assert_ids_and_names(assert, elem);
        const new_row = rows(elem).first();
        assert.true(new_row.hasClass('row-moved'));
        run_timeouts(assert);
        assert.false(new_row.hasClass('row-moved'));
    });

    QUnit.test('add row highlights new row', (assert) => {
        elem = create_dict(2);
        new DictWidget(elem);
        const evt = click($('a.dict_row_add', rows(elem).first()));
        assert.true(evt.isDefaultPrevented());
        assert.deepEqual(row_keys(elem), ['key0', '', 'key1']);
        assert_ids_and_names(assert, elem);
        const new_row = rows(elem).eq(1);
        assert.true(new_row.hasClass('row-moved'));
        assert.false(rows(elem).first().hasClass('row-moved'));
        run_timeouts(assert);
        assert.false(new_row.hasClass('row-moved'));
    });

    QUnit.test('move row up highlights row', (assert) => {
        elem = create_dict(2);
        new DictWidget(elem);
        const row = rows(elem).last();
        const evt = click($('a.dict_row_up', row));
        assert.true(evt.isDefaultPrevented());
        assert.deepEqual(row_keys(elem), ['key1', 'key0']);
        assert_ids_and_names(assert, elem);
        assert.true(row.hasClass('row-moved'));
        run_timeouts(assert);
        assert.false(row.hasClass('row-moved'));
    });

    QUnit.test('move row down highlights row', (assert) => {
        elem = create_dict(2);
        new DictWidget(elem);
        const row = rows(elem).first();
        const evt = click($('a.dict_row_down', row));
        assert.true(evt.isDefaultPrevented());
        assert.deepEqual(row_keys(elem), ['key1', 'key0']);
        assert_ids_and_names(assert, elem);
        assert.true(row.hasClass('row-moved'));
        run_timeouts(assert);
        assert.false(row.hasClass('row-moved'));
    });

    QUnit.test('register_array_subscribers', (assert) => {
        const subscribers = {};
        window.yafowil_array = {
            on_array_event: (evt_name, evt_function) => {
                subscribers[evt_name] = evt_function;
            },
            inside_template(node) {
                return node.parents('.arraytemplate').length > 0;
            },
        };
        register_array_subscribers();

        const container = $('<div><div class="arraytemplate" /></div>').appendTo('body');
        const template = $('<table class="dictwidget" />').appendTo($('.arraytemplate', container));
        elem = $('<table class="dictwidget" />').appendTo(container);
        subscribers.on_add(null, container);
        assert.strictEqual(template.data('yafowil-dict'), undefined);
        assert.true(elem.data('yafowil-dict') instanceof DictWidget);
        container.remove();
    });

    QUnit.test('register_array_subscribers with legacy array hooks', (assert) => {
        window.yafowil = { array: { hooks: { add: {} } } };
        register_array_subscribers();
        assert.strictEqual(window.yafowil.array.hooks.add.dictwidget_binder, DictWidget.initialize);
    });

    QUnit.test('register_array_subscribers without yafowil namespace', (assert) => {
        // no global ``yafowil`` if the widgets are used as ES modules
        register_array_subscribers();
        assert.strictEqual(window.yafowil, undefined);
        assert.strictEqual(window.yafowil_array, undefined);
    });

    QUnit.test('register_array_subscribers without array widget', (assert) => {
        window.yafowil = {};
        register_array_subscribers();
        assert.deepEqual(window.yafowil, {});
    });
});
