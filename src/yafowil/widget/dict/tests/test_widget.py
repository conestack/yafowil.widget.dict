from node.utils import UNSET
from odict import odict
from yafowil.base import ExtractionError
from yafowil.base import factory
from yafowil.compat import IS_PY2
from yafowil.tests import fxml
from yafowil.tests import YafowilTestCase
import os
import unittest


if not IS_PY2:
    from importlib import reload


def np(path):
    return path.replace('/', os.path.sep)


class TestDictWidget(YafowilTestCase):

    def setUp(self):
        super(TestDictWidget, self).setUp()
        from yafowil.widget import dict
        from yafowil.widget.dict import widget
        reload(widget)
        dict.register()

    def test_empty_dict(self):
        # Create empty Dict widget
        widget = factory(
            'dict',
            name='mydict',
            props={
                'key_label': 'Key',
                'value_label': 'Value',
            })
        result = widget()
        self.assertEqual(widget.treerepr().split('\n'), [
            "<class 'yafowil.base.Widget'>: mydict",
            "  <class 'yafowil.base.Widget'>: exists",
            "  <class 'yafowil.base.Widget'>: wrapper",
            "    <class 'yafowil.base.Widget'>: table",
            "      <class 'yafowil.base.Widget'>: head",
            "        <class 'yafowil.base.Widget'>: row",
            "          <class 'yafowil.base.Widget'>: key",
            "          <class 'yafowil.base.Widget'>: value",
            "          <class 'yafowil.base.Widget'>: actions",
            "      <class 'yafowil.base.Widget'>: body",
            ""
        ])

        self.checkOutput("""
        <div>
          <input class="hidden" id="input-mydict-exists" name="mydict.exists"
                 type="hidden" value="1"/>
          <fieldset class="card card-body p-0">
            <table class="dictwidget key-keyfield value-valuefield"
                   id="dictwidget_mydict.entry">
              <thead>
                <tr>
                  <th>Key</th>
                  <th>Value</th>
                  <th class="actions">
                    <div class="dict_actions">
                      <a class="dict_row_add" href="#">
                        <span class="icon-plus-sign"> </span>
                      </a>
                    </div>
                  </th>
                </tr>
              </thead>
              <tbody/>
            </table>
          </fieldset>
        </div>
        """, fxml('<div>' + result + '</div>'))

    def test_key_label_and_value_label_callables(self):
        # ``key_label`` and ``value_label`` may be callables
        widget = factory(
            'dict',
            name='mydict',
            props={
                'key_label': lambda w, d: 'Computed Key',
                'value_label': lambda w, d: 'Computed Value'
            })
        rendered = fxml('<div>{}</div>'.format(widget()))
        self.assertTrue(rendered.find('Computed Key') > -1)
        self.assertTrue(rendered.find('Computed Value') > -1)

    def test_bc_head_property(self):
        # Test B/C ``head`` property
        widget = factory(
            'dict',
            name='mydict',
            props={
                'head': {
                    'key': 'B/C Key',
                    'value': 'B/C Value',
                }
            })
        rendered = fxml('<div>{}</div>'.format(widget()))
        self.assertTrue(rendered.find('B/C Key') > -1)
        self.assertTrue(rendered.find('B/C Value') > -1)

    def test_bc_head_property_callables(self):
        widget = factory(
            'dict',
            name='mydict',
            props={
                'head': {
                    'key': lambda w, d: 'Computed B/C Key',
                    'value': lambda w, d: 'Computed B/C Value',
                }
            })
        rendered = fxml('<div>{}</div>'.format(widget()))
        self.assertTrue(rendered.find('Computed B/C Key') > -1)
        self.assertTrue(rendered.find('Computed B/C Value') > -1)

    def test_skip_labels(self):
        widget = factory('dict', name='mydict')
        rendered = fxml('<div>{}</div>'.format(widget()))
        # search for empty th
        index = rendered.find('<th> </th>')
        self.assertTrue(index > -1)
        # search for second empty th
        self.assertTrue(rendered.find('<th> </th>', index + 1) > index)

    def test_dict_with_preset_values(self):
        # Create dict widget with preset values
        widget = factory(
            'dict',
            name='mydict',
            value=odict([('key1', 'Value1'), ('key2', 'Value2')]),
            props={
                'key_label': 'Key',
                'value_label': 'Value',
            })
        rendered = widget()
        self.assertEqual(widget.treerepr().split('\n'), [
            "<class 'yafowil.base.Widget'>: mydict",
            "  <class 'yafowil.base.Widget'>: exists",
            "  <class 'yafowil.base.Widget'>: wrapper",
            "    <class 'yafowil.base.Widget'>: table",
            "      <class 'yafowil.base.Widget'>: head",
            "        <class 'yafowil.base.Widget'>: row",
            "          <class 'yafowil.base.Widget'>: key",
            "          <class 'yafowil.base.Widget'>: value",
            "          <class 'yafowil.base.Widget'>: actions",
            "      <class 'yafowil.base.Widget'>: body",
            "        <class 'yafowil.base.Widget'>: entry0",
            "          <class 'yafowil.base.Widget'>: key",
            "          <class 'yafowil.base.Widget'>: value",
            "          <class 'yafowil.base.Widget'>: actions",
            "        <class 'yafowil.base.Widget'>: entry1",
            "          <class 'yafowil.base.Widget'>: key",
            "          <class 'yafowil.base.Widget'>: value",
            "          <class 'yafowil.base.Widget'>: actions",
            ""
        ])
        self.checkOutput("""
        <div>
          ...
          <tbody>
            <tr>
              <td class="key">
                <input class="keyfield" id="input-mydict-entry0-key"
                       name="mydict.entry0.key" type="text" value="key1"/>
              </td>
              <td class="value">
                <input class="valuefield" id="input-mydict-entry0-value"
                       name="mydict.entry0.value" type="text" value="Value1"/>
              </td>
              <td class="actions">
                <div class="dict_actions">
                  <a class="dict_row_add" href="#">
                    <span class="icon-plus-sign"> </span>
                  </a>
                  <a class="dict_row_remove" href="#">
                    <span class="icon-minus-sign"> </span>
                  </a>
                  <a class="dict_row_up" href="#">
                    <span class="icon-circle-arrow-up"> </span>
                  </a>
                  <a class="dict_row_down" href="#">
                    <span class="icon-circle-arrow-down"> </span>
                  </a>
                </div>
              </td>
            </tr>
            <tr>
              <td class="key">
                <input class="keyfield" id="input-mydict-entry1-key"
                       name="mydict.entry1.key" type="text" value="key2"/>
              </td>
              <td class="value">
                <input class="valuefield" id="input-mydict-entry1-value"
                       name="mydict.entry1.value" type="text" value="Value2"/>
              </td>
              <td class="actions">
                <div class="dict_actions">
                  ...
                </div>
              </td>
            </tr>
          </tbody>
          ...
        </div>
        """, fxml('<div>{}</div>'.format(rendered)))

    def test_unset_extraction(self):
        widget = factory('dict', name='mydict')
        request = {}
        data = widget.extract(request)
        self.assertEqual(data.extracted, UNSET)

    def test_empty_extraction(self):
        widget = factory('dict', name='mydict')
        request = {
            'mydict.exists': '1'
        }
        data = widget.extract(request=request)
        self.assertEqual(data.extracted, odict())

    def test_non_empty_extraction(self):
        widget = factory('dict', name='mydict')
        request = {
            'mydict.exists': '1',
            'mydict.entry0.key': 'key1',
            'mydict.entry0.value': 'Value1',
            'mydict.entry1.key': 'key2',
            'mydict.entry1.value': 'Value2',
        }
        data = widget.extract(request=request)
        self.assertEqual(
            data.extracted,
            odict([('key1', 'Value1'), ('key2', 'Value2')])
        )
        rendered = widget(data=data)
        self.assertTrue(rendered.find('value="Value1"') > -1)
        self.assertTrue(rendered.find('value="Value2"') > -1)

    def test_override_extraction(self):
        widget = factory(
            'dict',
            name='mydict',
            value=odict([('key1', 'Value1'), ('key2', 'Value2')])
        )
        request = {
            'mydict.exists': '1',
            'mydict.entry0.key': 'key1',
            'mydict.entry0.value': 'Value1',
            'mydict.entry1.key': 'key2',
            'mydict.entry1.value': 'New Value2',
        }
        data = widget.extract(request=request)
        self.assertEqual(
            data.extracted,
            odict([('key1', 'Value1'), ('key2', 'New Value2')])
        )
        rendered = widget(data=data)
        self.assertTrue(rendered.find('value="Value1"') > -1)
        self.assertTrue(rendered.find('value="New Value2"') > -1)

    def test_entries_increased_extraction(self):
        widget = factory(
            'dict',
            name='mydict',
            value=odict([('key1', 'Value1')])
        )
        request = {
            'mydict.exists': '1',
            'mydict.entry0.key': 'key1',
            'mydict.entry0.value': 'Value1',
            'mydict.entry1.key': 'key2',
            'mydict.entry1.value': 'Value2',
        }
        data = widget.extract(request=request)
        self.assertEqual(
            data.extracted,
            odict([('key1', 'Value1'), ('key2', 'Value2')])
        )
        rendered = widget(data=data)
        self.assertTrue(rendered.find('value="Value1"') > -1)
        self.assertTrue(rendered.find('value="Value2"') > -1)

    def test_entries_decreased_extraction(self):
        widget = factory(
            'dict',
            name='mydict',
            value=odict([('key1', 'Value1'), ('key2', 'Value2')])
        )
        request = {
            'mydict.exists': '1',
            'mydict.entry0.key': 'key1',
            'mydict.entry0.value': 'Value1'
        }
        data = widget.extract(request=request)
        self.assertEqual(
            data.extracted,
            odict([('key1', 'Value1')])
        )
        rendered = widget(data=data)
        self.assertTrue(rendered.find('value="Value1"') > -1)
        self.assertFalse(rendered.find('value="Value2"') > -1)

    def test_empty_keys_ignored_extraction(self):
        widget = factory(
            'dict',
            name='mydict',
            value=odict([('key1', 'Value1'), ('key2', 'Value2')])
        )
        request = {
            'mydict.exists': '1',
            'mydict.entry0.key': 'key1',
            'mydict.entry0.value': 'New Value1',
            'mydict.entry1.key': '',
            'mydict.entry1.value': 'New Value2',
        }
        data = widget.extract(request=request)
        self.assertEqual(
            data.extracted,
            odict([('key1', 'New Value1')])
        )
        rendered = widget(data=data)
        self.assertTrue(rendered.find('value="New Value1"') > -1)
        self.assertFalse(rendered.find('value="New Value2"') > -1)

    def test_unset_required_extraction(self):
        widget = factory(
            'dict',
            name='mydict',
            props={
                'required': 'Dict entires required'
            })
        request = {}
        data = widget.extract(request)
        self.assertEqual(data.extracted, UNSET)
        self.assertFalse(data.has_errors)

    def test_empty_required_extraction(self):
        widget = factory(
            'dict',
            name='mydict',
            props={
                'required': 'Dict entries required'
            })
        request = {
            'mydict.exists': '1'
        }
        data = widget.extract(request)
        self.assertEqual(data.extracted, odict())
        self.assertTrue(data.has_errors)
        self.assertEqual(data.errors, [ExtractionError('Dict entries required')])

    def test_non_empty_required_extraction(self):
        widget = factory(
            'dict',
            name='mydict',
            props={
                'required': 'Dict entries required'
            })
        request = {
            'mydict.exists': '1',
            'mydict.entry0.key': 'key1',
            'mydict.entry0.value': 'Value1'
        }
        data = widget.extract(request=request)
        self.assertEqual(data.extracted, odict([('key1', 'Value1')]))
        self.assertFalse(data.has_errors)

    def test_override_required_extraction(self):
        widget = factory(
            'dict',
            name='mydict',
            value=odict([('key1', 'Value1'), ('key2', 'Value2')]),
            props={
                'required': 'Dict entries required'
            })
        request = {
            'mydict.exists': '1'
        }
        data = widget.extract(request=request)
        self.assertEqual(data.extracted, odict())
        self.assertTrue(data.has_errors)
        self.assertEqual(data.errors, [ExtractionError('Dict entries required')])
        rendered = widget(data=data)
        self.assertFalse(rendered.find('value="Value1"') > -1)
        self.assertFalse(rendered.find('value="Value2"') > -1)
        self.assertTrue(rendered.find('<tbody></tbody>') > -1)

    def test_static_dict(self):
        widget = factory(
            'error:dict',
            name='mydict',
            value=odict([('k1', 'v1')]),
            props={
                'static': True,
                'key_label': 'Key',
                'value_label': 'Value'
            })
        rendered = widget()
        self.assertEqual(widget.treerepr().split('\n'), [
            "<class 'yafowil.base.Widget'>: mydict",
            "  <class 'yafowil.base.Widget'>: exists",
            "  <class 'yafowil.base.Widget'>: wrapper",
            "    <class 'yafowil.base.Widget'>: table",
            "      <class 'yafowil.base.Widget'>: head",
            "        <class 'yafowil.base.Widget'>: row",
            "          <class 'yafowil.base.Widget'>: key",
            "          <class 'yafowil.base.Widget'>: value",
            "      <class 'yafowil.base.Widget'>: body",
            "        <class 'yafowil.base.Widget'>: entry0",
            "          <class 'yafowil.base.Widget'>: key",
            "          <class 'yafowil.base.Widget'>: value",
            ""
        ])
        self.checkOutput("""
        <div>
          <input class="hidden" id="input-mydict-exists"
                        name="mydict.exists" type="hidden" value="1"/>
          <fieldset class="card card-body p-0">
            <table class="dictwidget key-keyfield value-valuefield"
                   id="dictwidget_mydict.entry">
              <thead>
                <tr>
                  <th>Key</th>
                  <th>Value</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td class="key">
                    <input class="keyfield" disabled="disabled"
                           id="input-mydict-entry0-key"
                           name="mydict.entry0.key" type="text" value="k1"/>
                  </td>
                  <td class="value">
                    <input class="valuefield" id="input-mydict-entry0-value"
                           name="mydict.entry0.value" type="text" value="v1"/>
                  </td>
                </tr>
              </tbody>
            </table>
          </fieldset>
        </div>
        """, fxml('<div>{}</div>'.format(rendered)))

    def test_static_extraction(self):
        # Static dict extraction. Disabled form fields are not transmitted, but
        # since order is fixed, dict can be reconstructed from original value
        widget = factory(
            'dict',
            name='mydict',
            value=odict([('k1', 'v1')]),
            props={
                'static': True,
                'key_label': 'Key',
                'value_label': 'Value'
            })
        request = {
            'mydict.exists': '1',
            'mydict.entry0.value': 'New Value1',
        }
        data = widget.extract(request=request)
        self.assertEqual(data.extracted, odict([('k1', 'New Value1')]))

    def test_static_required_extraction_error(self):
        # if static dict is required, dict values must not be empty
        widget = factory(
            'error:dict',
            name='mydict',
            value=odict([('k1', 'v1')]),
            props={
                'required': True,
                'static': True,
                'key_label': 'Key',
                'value_label': 'Value'
            })
        request = {
            'mydict.exists': '1',
            'mydict.entry0.value': '',
        }
        data = widget.extract(request=request)
        self.assertTrue(data.has_errors)
        self.assertEqual(
            data.errors,
            [ExtractionError('Dict values must not be empty')]
        )
        # custom required message
        widget.attrs['required'] = 'Doh! no values.'
        data = widget.extract(request=request)
        self.assertTrue(data.has_errors)
        self.assertEqual(
            data.errors,
            [ExtractionError('Doh! no values.')]
        )
        # check rendered
        rendered = widget(data=data)
        expected = '<div class="errormessage">Doh! no values.</div>'
        self.assertTrue(rendered.find(expected) > -1)
        expected = 'name="mydict.entry0.value" type="text" value=""'
        self.assertTrue(rendered.find(expected) > -1)

    def test_static_required_extraction_success(self):
        # if static dict is required, dict values must not be empty
        widget = factory(
            'error:dict',
            name='mydict',
            value=odict([('k1', 'v1')]),
            props={
                'required': True,
                'static': True,
                'key_label': 'Key',
                'value_label': 'Value'
            })
        # check valid extraction
        request = {
            'mydict.exists': '1',
            'mydict.entry0.value': 'Value1',
        }
        data = widget.extract(request=request)
        self.assertFalse(data.has_errors)
        self.assertEqual(
            data.extracted,
            odict([('k1', 'Value1')])
        )
        # check rendered
        rendered = widget(data=data)
        expected = '<div class="errormessage">'
        self.assertFalse(rendered.find(expected) > -1)
        expected = 'name="mydict.entry0.value" type="text" value="Value1"'
        self.assertTrue(rendered.find(expected) > -1)

    def test_datatype_extraction(self):
        widget = factory(
            'error:dict',
            name='mydict',
            props={
                'key_type': int,
                'value_type': int
            })
        request = {
            'mydict.exists': '1',
            'mydict.entry0.key': '0',
            'mydict.entry0.value': '1',
        }
        data = widget.extract(request=request)
        self.assertFalse(data.has_errors)
        self.assertEqual(
            data.extracted,
            odict([(0, 1)])
        )
        request = {
            'mydict.exists': '1',
            'mydict.entry0.key': 'a',
            'mydict.entry0.value': '1',
        }
        data = widget.extract(request=request)
        self.assertEqual(
            data.errors,
            [ExtractionError('Key a is not a valid integer.',)]
        )
        request = {
            'mydict.exists': '1',
            'mydict.entry0.key': '0',
            'mydict.entry0.value': 'b',
        }
        data = widget.extract(request=request)
        self.assertEqual(
            data.errors,
            [ExtractionError('Value b is not a valid integer.',)]
        )

    def test_display_dict(self):
        widget = factory(
            'dict',
            name='display_dict',
            value=odict([('foo', 'Foo'), ('bar', 'Bar')]),
            props={
                'key_label': 'Key',
                'value_label': 'Value',
            },
            mode='display')
        self.checkOutput("""
        <div>
          <h5>Key: Value</h5>
          <dl>
            <dt>foo</dt>
            <dd>Foo</dd>
            <dt>bar</dt>
            <dd>Bar</dd>
          </dl>
        </div>
        """, fxml('<div>{}</div>'.format(widget())))

    def test_display_empty_value(self):
        widget = factory(
            'dict',
            name='display_dict',
            props={
                'key_label': 'Key',
                'value_label': 'Value'
            },
            mode='display')
        self.checkOutput("""
        <div>
          <h5>Key: Value</h5>
          <dl/>
        </div>
        """, fxml('<div>{}</div>'.format(widget())))

    def test_display_callable_labels(self):
        widget = factory(
            'dict',
            name='display_dict',
            props={
                'key_label': lambda w, d: 'Computed Key',
                'value_label': lambda w, d: 'Computed Value'
            },
            mode='display')
        self.checkOutput("""
        <div>
          <h5>Computed Key: Computed Value</h5>
          <dl/>
        </div>
        """, fxml('<div>{}</div>'.format(widget())))

    def test_display_bc_labels(self):
        widget = factory(
            'dict',
            name='display_dict',
            props={
                'head': {
                    'key': 'B/C Key',
                    'value': 'B/C Value',
                }
            },
            mode='display')
        self.checkOutput("""
        <div>
          <h5>B/C Key: B/C Value</h5>
          <dl/>
        </div>
        """, fxml('<div>{}</div>'.format(widget())))

    def test_display_computed_bc_labels(self):
        widget = factory(
            'dict',
            name='display_dict',
            props={
                'head': {
                    'key': lambda w, d: 'Computed B/C Key',
                    'value': lambda w, d: 'Computed B/C Value',
                }
            },
            mode='display')
        self.checkOutput("""
        <div>
          <h5>Computed B/C Key: Computed B/C Value</h5>
          <dl/>
        </div>
        """, fxml('<div>{}</div>'.format(widget())))

    def test_display_renderer_no_labels(self):
        widget = factory(
            'dict',
            name='display_dict',
            mode='display'
        )
        self.checkOutput("""
        <div>
          <dl/>
        </div>
        """, fxml('<div>{}</div>'.format(widget())))

    def test_resources(self):
        factory.theme = 'default'
        resources = factory.get_resources('yafowil.widget.dict')
        self.assertTrue(resources.directory.endswith(np('/dict/resources')))
        self.assertEqual(resources.name, 'yafowil.widget.dict')
        self.assertEqual(resources.path, 'yafowil-dict')

        scripts = resources.scripts
        self.assertEqual(len(scripts), 1)

        self.assertTrue(scripts[0].directory.endswith(np('/dict/resources')))
        self.assertEqual(scripts[0].path, 'yafowil-dict')
        self.assertEqual(scripts[0].file_name, 'default/widget.min.js')
        self.assertTrue(os.path.exists(scripts[0].file_path))

        styles = resources.styles
        self.assertEqual(len(styles), 1)

        self.assertTrue(
            styles[0].directory.endswith(np('/dict/resources/default'))
        )
        self.assertEqual(styles[0].path, 'yafowil-dict/default')
        self.assertEqual(styles[0].file_name, 'widget.css')
        self.assertTrue(os.path.exists(styles[0].file_path))

        factory.theme = 'bootstrap3'
        resources = factory.get_resources('yafowil.widget.dict')
        self.assertTrue(resources.directory.endswith(np('/dict/resources')))
        self.assertEqual(resources.name, 'yafowil.widget.dict')
        self.assertEqual(resources.path, 'yafowil-dict')

        scripts = resources.scripts
        self.assertEqual(len(scripts), 1)

        self.assertTrue(scripts[0].directory.endswith(np('/dict/resources')))
        self.assertEqual(scripts[0].path, 'yafowil-dict')
        self.assertEqual(scripts[0].file_name, 'default/widget.min.js')
        self.assertTrue(os.path.exists(scripts[0].file_path))

        styles = resources.styles
        self.assertEqual(len(styles), 1)

        self.assertTrue(
            styles[0].directory.endswith(np('/dict/resources/bootstrap'))
        )
        self.assertEqual(styles[0].path, 'yafowil-dict/bootstrap')
        self.assertEqual(styles[0].file_name, 'widget.css')
        self.assertTrue(os.path.exists(styles[0].file_path))

        factory.theme = 'plone5'
        resources = factory.get_resources('yafowil.widget.dict')
        self.assertTrue(resources.directory.endswith(np('/dict/resources')))
        self.assertEqual(resources.name, 'yafowil.widget.dict')
        self.assertEqual(resources.path, 'yafowil-dict')

        scripts = resources.scripts
        self.assertEqual(len(scripts), 1)

        self.assertTrue(scripts[0].directory.endswith(np('/dict/resources')))
        self.assertEqual(scripts[0].path, 'yafowil-dict')
        self.assertEqual(scripts[0].file_name, 'default/widget.min.js')
        self.assertTrue(os.path.exists(scripts[0].file_path))

        styles = resources.styles
        self.assertEqual(len(styles), 1)

        self.assertTrue(
            styles[0].directory.endswith(np('/dict/resources/plone5'))
        )
        self.assertEqual(styles[0].path, 'yafowil-dict/plone5')
        self.assertEqual(styles[0].file_name, 'widget.css')
        self.assertTrue(os.path.exists(styles[0].file_path))


if __name__ == '__main__':
    unittest.main()
