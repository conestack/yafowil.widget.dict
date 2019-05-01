from node.utils import UNSET
from odict import odict
from yafowil.base import ExtractionError
from yafowil.base import factory
from yafowil.compat import IS_PY2
from yafowil.tests import fxml
from yafowil.tests import YafowilTestCase
import unittest
import yafowil.loader


if not IS_PY2:
    from importlib import reload


class TestDictWidget(YafowilTestCase):

    def setUp(self):
        super(TestDictWidget, self).setUp()
        from yafowil.widget.dict import widget
        reload(widget)

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
            "  <class 'yafowil.base.Widget'>: table",
            "    <class 'yafowil.base.Widget'>: head",
            "      <class 'yafowil.base.Widget'>: row",
            "        <class 'yafowil.base.Widget'>: key",
            "        <class 'yafowil.base.Widget'>: value",
            "        <class 'yafowil.base.Widget'>: actions",
            "    <class 'yafowil.base.Widget'>: body",
            ""
        ])
        self.check_output("""
        <div>
          <input class="hidden" name="mydict" type="hidden" value=""/>
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
        rendered = fxml('<div>' + widget() + '</div>')
        self.assertTrue(rendered.find('Computed Key') > -1)
        self.assertTrue(rendered.find('Computed Value') > -1)

    def test_key_label_and_value_label_bc_callables(self):
        # test B/C callable signature
        widget = factory(
            'dict',
            name='mydict',
            props={
                'key_label': lambda: 'B/C Computed Key',
                'value_label': lambda: 'B/C Computed Value'
            })
        rendered = fxml('<div>' + widget() + '</div>')
        self.assertTrue(rendered.find('B/C Computed Key') > -1)
        self.assertTrue(rendered.find('B/C Computed Value') > -1)

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
        rendered = fxml('<div>' + widget() + '</div>')
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
        rendered = fxml('<div>' + widget() + '</div>')
        self.assertTrue(rendered.find('Computed B/C Key') > -1)
        self.assertTrue(rendered.find('Computed B/C Value') > -1)

    def test_bc_head_property_bc_callables(self):
        widget = factory(
            'dict',
            name='mydict',
            props={
                'head': {
                    'key': lambda: 'B/C Computed B/C Key',
                    'value': lambda: 'B/C Computed B/C Value',
                }
            })
        rendered = fxml('<div>' + widget() + '</div>')
        self.assertTrue(rendered.find('B/C Computed B/C Key') > -1)
        self.assertTrue(rendered.find('B/C Computed B/C Value') > -1)

    def test_skip_labels(self):
        widget = factory('dict', name='mydict')
        rendered = fxml('<div>' + widget() + '</div>')
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
        result = widget()
        self.assertEqual(widget.treerepr().split('\n'), [
            "<class 'yafowil.base.Widget'>: mydict",
            "  <class 'yafowil.base.Widget'>: exists",
            "  <class 'yafowil.base.Widget'>: table",
            "    <class 'yafowil.base.Widget'>: head",
            "      <class 'yafowil.base.Widget'>: row",
            "        <class 'yafowil.base.Widget'>: key",
            "        <class 'yafowil.base.Widget'>: value",
            "        <class 'yafowil.base.Widget'>: actions",
            "    <class 'yafowil.base.Widget'>: body",
            "      <class 'yafowil.base.Widget'>: entry0",
            "        <class 'yafowil.base.Widget'>: key",
            "        <class 'yafowil.base.Widget'>: value",
            "        <class 'yafowil.base.Widget'>: actions",
            "      <class 'yafowil.base.Widget'>: entry1",
            "        <class 'yafowil.base.Widget'>: key",
            "        <class 'yafowil.base.Widget'>: value",
            "        <class 'yafowil.base.Widget'>: actions",
            ""
        ])
        self.check_output("""
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
        """, fxml('<div>' + result + '</div>'))

    def test_unset_extraction(self):
        widget = factory('dict', name='mydict')
        widget()  # need to call widget in order to instanciate subwidgets
        request = {}
        data = widget.extract(request)
        self.assertEqual(data.extracted, UNSET)

    def test_empty_extraction(self):
        widget = factory('dict', name='mydict')
        widget()  # need to call widget in order to instanciate subwidgets
        request = {
            'mydict': ''  # exists marker
        }
        data = widget.extract(request=request)
        self.assertEqual(data.extracted, odict())

    def test_non_empty_extraction(self):
        widget = factory('dict', name='mydict')
        widget()  # need to call widget in order to instanciate subwidgets
        request = {
            'mydict': '',  # exists marker
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
        widget()  # need to call widget in order to instanciate subwidgets
        request = {
            'mydict': '',  # exists marker
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
        widget()  # need to call widget in order to instanciate subwidgets
        request = {
            'mydict': '',  # exists marker
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
        widget()  # need to call widget in order to instanciate subwidgets
        request = {
            'mydict': '',  # exists marker
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
        widget()  # need to call widget in order to instanciate subwidgets
        request = {
            'mydict': '',  # exists marker
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
        widget()  # need to call widget in order to instanciate subwidgets
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
        widget()  # need to call widget in order to instanciate subwidgets
        request = {
            'mydict': ''  # exists marker
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
        widget()  # need to call widget in order to instanciate subwidgets
        request = {
            'mydict': '',  # exists marker
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
        widget()  # need to call widget in order to instanciate subwidgets
        request = {
            'mydict': ''  # exists marker
        }
        data = widget.extract(request=request)
        self.assertEqual(data.extracted, odict())
        self.assertTrue(data.has_errors)
        self.assertEqual(data.errors, [ExtractionError('Dict entries required')])
        rendered = widget(data=data)
        self.assertFalse(rendered.find('value="Value1"') > -1)
        self.assertFalse(rendered.find('value="Value2"') > -1)

    def _test_render_static_dict(self):
        # Use dict widget as static widget
        form = factory(
            'form',
            name='myform',
            props={
                'action': 'myaction'
            })
        form['mydict'] = factory(
            'error:dict',
            value=odict([('k1', 'v1')]),
            props={
                'required': 'I am required',
                'static': True,
                'key_label': 'Key',
                'value_label': 'Value'
            })
        self.check_output("""
        <form action="myaction" enctype="multipart/form-data" id="form-myform"
              method="post" novalidate="novalidate">
          <input class="hidden" id="input-myform-mydict-exists"
                 name="myform.mydict.exists" type="hidden" value="1"/>
          <table class="dictwidget key-keyfield value-valuefield"
                 id="dictwidget_myform.mydict.entry">
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
                         id="input-myform-mydict-entry0-key"
                         name="myform.mydict.entry0.key"
                         type="text" value="k1"/>
                </td>
                <td class="value">
                  <input class="valuefield"
                         id="input-myform-mydict-entry0-value"
                         name="myform.mydict.entry0.value"
                         type="text" value="v1"/>
                </td>
              </tr>
            </tbody>
          </table>
        </form>
        """, fxml(form()))

    def _test_extract_static_dict(self):
        # Static dict extraction. Disabled form fields are not transmitted, but
        # since order is fixed dict could be reconstructed from original value
        form = factory(
            'form',
            name='myform',
            props={
                'action': 'myaction'
            })
        form['mydict'] = factory(
            'error:dict',
            value=odict([('k1', 'v1')]),
            props={
                'static': True,
                'key_label': 'Key',
                'value_label': 'Value'
            })

        request = {
            'myform.mydict.exists': '1',
            'myform.mydict.entry0.value': 'New Value 1',
        }
        data = form.extract(request=request)
        self.assertEqual(
            data.fetch('myform.mydict').extracted,
            odict([('k1', 'New Value 1')])
        )

        # Since its static, we expect an extraction error if someone tries to
        # add values
        request = {
            'myform.mydict.exists': '1',
            'myform.mydict.entry0.value': 'New Value 1',
            'myform.mydict.entry1.key': 'Wrong Key 2',
            'myform.mydict.entry1.value': 'Wrong Value 2',
        }
        data = form.extract(request=request)
        self.assertEqual(
            data['mydict'].errors,
            [ExtractionError('Invalid number of static values')]
        )

    def _test_required_static_dict(self):
        # Static dicts required. By default checks if there's a value in
        # every entry
        form = factory(
            'form',
            name='myform',
            props={
                'action': 'myaction'
            })
        form['mydict'] = factory(
            'error:dict',
            value=odict([('k1', 'v1')]),
            props={
                'required': 'I am required',
                'static': True,
                'key_label': 'Key',
                'value_label': 'Value'
            })

        request = {
            'myform.mydict.exists': '1',
        }
        data = form.extract(request=request)
        self.assertEqual(
            data.fetch('myform.mydict').errors,
            [ExtractionError('I am required')]
        )

        request = {
            'myform.mydict.exists': '1',
            'myform.mydict.entry0.value': '',
        }
        data = form.extract(request=request)
        self.assertEqual(
            data.fetch('myform.mydict').errors,
            [ExtractionError('I am required')]
        )

        # Static required rendering
        self.check_output("""
        <form action="myaction" enctype="multipart/form-data" id="form-myform"
              method="post" novalidate="novalidate">
          <div class="error">
            <div class="errormessage">I am required</div>
            <input class="hidden" id="input-myform-mydict-exists"
                   name="myform.mydict.exists" type="hidden" value="1"/>
            <table class="dictwidget key-keyfield value-valuefield"
                   id="dictwidget_myform.mydict.entry">
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
                           id="input-myform-mydict-entry0-key"
                           name="myform.mydict.entry0.key"
                           type="text" value="k1"/>
                  </td>
                  <td class="value">
                    <input class="valuefield"
                           id="input-myform-mydict-entry0-value"
                           name="myform.mydict.entry0.value"
                           type="text" value=""/>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </form>
        """, fxml(form(data)))

        # Required message not set directly in widget props
        form['mydict'].attrs['required'] = True
        request = {
            'myform.mydict.exists': '1',
            'myform.mydict.entry0.value': '',
        }
        data = form.extract(request=request)
        self.assertEqual(
            data.fetch('myform.mydict').errors,
            [ExtractionError('Mandatory field was empty')]
        )

    def _test_display_renderer(self):
        # Dict display renderer
        value = odict()
        value['foo'] = 'Foo'
        value['bar'] = 'Bar'
        widget = factory(
            'dict',
            name='display_dict',
            value=value,
            props={
                'key_label': 'Key',
                'value_label': 'Value',
            },
            mode='display')
        self.check_output("""
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

    def _test_display_renderer_empty_values(self):
        # Display dict empty values
        widget = factory(
            'dict',
            name='display_dict',
            props={
                'key_label': 'Key',
                'value_label': 'Value'
            },
            mode='display')
        self.check_output("""
        <div>
          <h5>Key: Value</h5>
          <dl/>
        </div>
        """, fxml('<div>{}</div>'.format(widget())))

    def _test_display_renderer_callable_labels(self):
        # Display dict callable labels
        widget = factory(
            'dict',
            name='display_dict',
            props={
                'key_label': lambda: 'Computed Key',
                'value_label': lambda: 'Computed Value'
            },
            mode='display')
        self.check_output("""
        <div>
          <h5>Computed Key: Computed Value</h5>
          <dl/>
        </div>
        """, fxml('<div>{}</div>'.format(widget())))

    def _test_display_renderer_bc_labels(self):
        # Display dict, B/C labels
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
        self.check_output("""
        <div>
          <h5>B/C Key: B/C Value</h5>
          <dl/>
        </div>
        """, fxml('<div>{}</div>'.format(widget())))

    def _test_display_renderer_computed_bc_labels(self):
        # Display dict, computed B/C labels
        widget = factory(
            'dict',
            name='display_dict',
            props={
                'head': {
                    'key': lambda: 'Computed B/C Key',
                    'value': lambda: 'Computed B/C Value',
                }
            },
            mode='display')
        self.check_output("""
        <div>
          <h5>Computed B/C Key: Computed B/C Value</h5>
          <dl/>
        </div>
        """, fxml('<div>{}</div>'.format(widget())))

    def _test_display_renderer_no_labels(self):
        # Display dict, no labels
        widget = factory(
            'dict',
            name='display_dict',
            mode='display'
        )
        self.check_output("""
        <div>
          <dl/>
        </div>
        """, fxml('<div>{}</div>'.format(widget())))


if __name__ == '__main__':
    unittest.main()                                          # pragma: no cover
