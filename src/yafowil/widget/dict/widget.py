from node.utils import UNSET
from odict import odict
from yafowil.base import ExtractionError
from yafowil.base import factory
from yafowil.base import fetch_value
from yafowil.compat import STR_TYPE
from yafowil.compound import compound_extractor
from yafowil.compound import compound_renderer
from yafowil.tsf import TSF
from yafowil.utils import attr_value
from yafowil.utils import css_managed_props
from yafowil.utils import managedprops


_ = TSF('yafowil.widget.dict')


ICON_CSS = {
    'add': 'icon-plus-sign',
    'remove': 'icon-minus-sign',
    'up': 'icon-circle-arrow-up',
    'down': 'icon-circle-arrow-down',
}

def actions_renderer(widget, data):
    tag = data.tag
    actions = list()
    for key in ['add', 'remove', 'up', 'down']:
        if widget.attrs.get(key):
            class_ = 'dict_row_%s' % key
            icon = tag('span', ' ', class_=ICON_CSS[key])
            action = tag('a', icon, href='#', class_=class_)
            actions.append(action)
    kw = dict(class_='dict_actions')
    return tag('div', *actions, **kw)


factory.register(
    'dict_actions',
    edit_renderers=[actions_renderer])

factory.doc['blueprint']['dict_actions'] = UNSET # dont document internal widget


@managedprops('static', 'table_class', *css_managed_props)
def dict_builder(widget, factory):
    table_classes = [widget.attrs['table_class'],
                     'key-{0}'.format(widget.attrs['key_class']),
                     'value-{0}'.format(widget.attrs['value_class'])]
    table = widget['table'] = factory('table', props={
        'structural': True,
        'class': ' '.join(table_classes),
    })
    head = table['head'] = factory('thead', props={
        'structural': True,
    })
    row = head['row'] = factory('tr', props={
        'structural': True,
    })
    key_label = widget.attrs.get('key_label', '')
    # B/C
    if not key_label:
        key_label = widget.attrs.get('head', {}).get('key', ' ')
    if callable(key_label):
        key_label = key_label()
    row['key'] = factory('th', props={
        'structural': True,
        'label': key_label,
    })
    value_label = widget.attrs.get('value_label', '')
    # B/C
    if not value_label:
        value_label = widget.attrs.get('head', {}).get('value', ' ')
    if callable(value_label):
        value_label = value_label()
    row['value'] = factory('th', props={
        'structural': True,
        'label': value_label,
    })
    if not widget.attrs['static']:
        row['actions'] = factory('th:dict_actions', props={
            'structural': True,
            'add': True,
            'class': 'actions',
        })
    table['body'] = factory('tbody', props={
        'structural': True,
    })


@managedprops('static', *css_managed_props)
def dict_edit_renderer(widget, data):
    static = widget.attrs['static']
    table = widget['table']
    table.attrs['id'] = 'dictwidget_%s.entry' % widget.dottedpath
    body = table['body']
    body.clear()
    if data.errors and static:
        basename = '%s.entry' % body.dottedpath
        value = extract_static(data, basename)
    else:
        value = fetch_value(widget, data)
    if not value:
        return
    i = 0
    for key, val in value.items():
        row = body['entry%i' % i] = factory('tr')
        k_props = {
            'td.class': 'key',
            'text.class': attr_value('key_class', widget, data),
        }
        if static:
            k_props['disabled'] = 'disabled'
        row['key'] = factory('td:text', value=key, name='key', props=k_props)
        row['value'] = factory('td:text', value=val, name='value', props={
            'td.class': 'value',
            'text.class': attr_value('value_class', widget, data),
        })
        if not static:
            row['actions'] = factory('td:dict_actions', props={
                'add': True,
                'remove': True,
                'up': True,
                'down': True,
                'class': 'actions',
            })
        i += 1


def raise_extraction_error(widget, data):
    required = attr_value('required', widget, data)
    if isinstance(required, STR_TYPE):
        raise ExtractionError(required)
    required_message = attr_value('required_message', widget, data)
    raise ExtractionError(required_message)


def extract_static(data, basename):
    request = data.request
    ret = odict()
    index = 0
    keys = data.value.keys()
    while True:
        valuename = '%s%i.value' % (basename, index)
        if valuename in request:
            if index >= len(keys):
                message = _('invalid_number_static_values',
                            default=u'Invalid number of static values')
                raise ExtractionError(message)
            ret[keys[index]] = request[valuename]
            index += 1
            continue
        break
    return ret


def extract_dynamic(data, basename):
    request = data.request
    ret = odict()
    index = 0
    while True:
        keyname = '%s%i.key' % (basename, index)
        valuename = '%s%i.value' % (basename, index)
        if keyname in request:
            key = request[keyname].strip()
            if key:
                ret[key] = request[valuename]
            index += 1
            continue
        break
    return ret

@managedprops('static', 'required')
def dict_extractor(widget, data):
    static = widget.attrs['static']
    body = widget['table']['body']
    compound_extractor(body, data)
    basename = '%s.entry' % body.dottedpath
    req = data.request
    index = 0
    if static:
        ret = extract_static(data, basename)
    else:
        ret = extract_dynamic(data, basename)
    if len(ret) == 0:
        ret = UNSET
    if attr_value('required', widget, data):
        if ret is UNSET:
            raise_extraction_error(widget, data)
        if static:
            for val in ret.values():
                if not val:
                    raise_extraction_error(widget, data)
    return ret


def dict_display_renderer(widget, data):
    value = data.value
    if not value:
        value = dict()
    values = list()
    for key, val in value.items():
        values.append(data.tag('dt', key) + data.tag('dd', val))
    head = u''
    key_label = widget.attrs.get('key_label')
    # B/C
    if not key_label:
        key_label = widget.attrs.get('head', {}).get('key', '')
    if callable(key_label):
        key_label = key_label()
    value_label = widget.attrs.get('value_label')
    # B/C
    if not value_label:
        value_label = widget.attrs.get('head', {}).get('value', '')
    if callable(value_label):
        value_label = value_label()
    if key_label and value_label:
        head = u'{}: {}'.format(
            data.tag.translate(key_label),
            data.tag.translate(value_label)
        )
        head = data.tag('h5', head)
    return head + data.tag('dl', *values)


factory.register(
    'dict',
    extractors=[dict_extractor],
    edit_renderers=[dict_edit_renderer, compound_renderer],
    display_renderers=[dict_display_renderer],
    builders=[dict_builder])

factory.doc['blueprint']['dict'] = \
"""Add-on widget `yafowil.widget.dict
<http://github.com/bluedynamics/yafowil.widget.dict/>`_.
"""

factory.defaults['dict.default'] = odict()

factory.defaults['dict.error_class'] = 'error'

factory.defaults['dict.message_class'] = 'errormessage'

factory.defaults['dict.table_class'] = 'dictwidget'
factory.doc['props']['dict.table_class'] = \
"""CSS classes rendered on dict table.
"""

factory.defaults['dict.key_class'] = 'keyfield'
factory.doc['props']['dict.key_class'] = \
"""CSS classes rendered on key input fields.
"""

factory.defaults['dict.value_class'] = 'valuefield'
factory.doc['props']['dict.value_class'] = \
"""CSS classes rendered on value input fields.
"""

factory.defaults['dict.key_label'] = UNSET
factory.doc['props']['dict.key_label'] = \
"""Label for dict keys column.
"""

factory.defaults['dict.value_label'] = UNSET
factory.doc['props']['dict.value_label'] = \
"""Label for dict values column.
"""

factory.defaults['dict.head'] = {}
factory.doc['props']['dict.head'] = \
"""B/C Labels for dict keys and values columns. Expect a dict containing
``key`` and ``value`` keys.
"""

factory.defaults['dict.static'] = False
"""Flag whether dict is immutable.
"""

factory.doc['props']['dict.static'] = \
"""Makes keys immutable.
"""
