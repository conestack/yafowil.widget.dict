from node.utils import UNSET
from odict import odict
from yafowil.base import ExtractionError
from yafowil.base import factory
from yafowil.base import fetch_value
from yafowil.common import generic_required_extractor
from yafowil.compat import STR_TYPE
from yafowil.compound import compound_renderer
from yafowil.datatypes import DATATYPE_LABELS
from yafowil.tsf import TSF
from yafowil.utils import attr_value
from yafowil.utils import callable_value
from yafowil.utils import css_managed_props
from yafowil.utils import managedprops


_ = TSF('yafowil.widget.dict')


ICON_CSS = {
    'add': 'icon-plus-sign',
    'remove': 'icon-minus-sign',
    'up': 'icon-circle-arrow-up',
    'down': 'icon-circle-arrow-down',
}
BS_ICON = {
    'add': 'bi-plus-circle-fill',
    'remove': 'bi-dash-circle-fill',
    'up': 'bi-arrow-up-circle-fill',
    'down': 'bi-arrow-down-circle-fill',
}


def actions_renderer(widget, data):
    tag = data.tag
    actions = list()
    icons = BS_ICON if factory.theme == 'bootstrap5' else ICON_CSS
    for key in ['add', 'remove', 'up', 'down']:
        if widget.attrs.get(key):
            class_ = 'dict_row_{}'.format(key)
            icon = tag('span', ' ', class_=icons[key])
            action = tag('a', icon, href='#', class_=class_)
            actions.append(action)
    kw = dict(class_='dict_actions')
    return tag('div', *actions, **kw)


factory.register(
    'dict_actions',
    edit_renderers=[
        actions_renderer
    ]
)

factory.doc['blueprint']['dict_actions'] = UNSET  # dont document internal widget


def dict_label(widget, data, name, bc_name):
    label = attr_value(name, widget, data)
    if not label:  # B/C
        label = callable_value(
            attr_value('head', widget, data, default={}).get(bc_name, ' '),
            widget,
            data
        )
    return label


def key_label(widget, data):
    return dict_label(widget, data, 'key_label', 'key')


def value_label(widget, data):
    return dict_label(widget, data, 'value_label', 'value')


@managedprops(
    'static',
    'scrollable',
    'table_class',
    'key_class',
    'value_class',
    'key_label',
    'value_label',
    'head',
    *css_managed_props)
def dict_edit_renderer(widget, data):
    widget['exists'] = factory('hidden', value='1')
    key_class = attr_value('key_class', widget, data)
    value_class = attr_value('value_class', widget, data)
    scrollable = attr_value('scrollable', widget, data)
    wrapper = widget['wrapper'] = factory(
        'fieldset',
        props={
            'structural': True,
            'class': 'card card-body p-0 scrollable-x' if scrollable else 'card card-body p-0'
        }
    )
    table = wrapper['table'] = factory(
        'table',
        props={
            'structural': True,
            'id': 'dictwidget_{}.entry'.format(widget.dottedpath),
            'class': ' '.join([
                attr_value('table_class', widget, data),
                'key-{0}'.format(key_class),
                'value-{0}'.format(value_class),
                'scrollable-content' if scrollable else ''
            ])
        })
    head = table['head'] = factory(
        'thead',
        props={
            'structural': True
        })
    row = head['row'] = factory(
        'tr',
        props={
            'structural': True
        })
    row['key'] = factory(
        'th',
        props={
            'structural': True,
            'label': key_label(widget, data)
        })
    row['value'] = factory(
        'th',
        props={
            'structural': True,
            'label': value_label(widget, data)
        })
    static = attr_value('static', widget, data)
    if not static:
        row['actions'] = factory(
            'th:dict_actions',
            props={
                'structural': True,
                'add': True,
                'class': 'actions'
            })
    body = table['body'] = factory(
        'tbody',
        props={
            'structural': True
        })
    value = fetch_value(widget, data)
    if not value:
        return
    i = 0
    for key, val in value.items():
        row = body['entry{}'.format(i)] = factory('tr')
        k_props = {
            'td.class': 'key',
            'text.class': key_class
        }
        if static:
            k_props['disabled'] = 'disabled'
        row['key'] = factory(
            'td:text',
            value=key,
            name='key',
            props=k_props
        )
        row['value'] = factory(
            'td:text',
            value=val,
            name='value',
            props={
                'td.class': 'value',
                'text.class': value_class
            })
        if not static:
            row['actions'] = factory(
                'td:dict_actions',
                props={
                    'add': True,
                    'remove': True,
                    'up': True,
                    'down': True,
                    'class': 'actions'
                })
        i += 1


@managedprops('key_label', 'value_label', 'head')
def dict_display_renderer(widget, data):
    value = data.value
    if not value:
        value = dict()
    values = list()
    for key, val in value.items():
        values.append(data.tag('dt', key) + data.tag('dd', val))
    head = u''
    k_label = key_label(widget, data)
    v_label = value_label(widget, data)
    if k_label.strip() and v_label.strip():
        head = u'{}: {}'.format(
            data.tag.translate(k_label),
            data.tag.translate(v_label)
        )
        head = data.tag('h5', head)
    return head + data.tag('dl', *values)


@managedprops('static')
def dict_extractor(widget, data):
    if '{}.exists'.format(widget.dottedpath) not in data.request:
        return UNSET
    extracted = odict()
    request = data.request
    base_name = '{}.entry'.format(widget.dottedpath)
    if attr_value('static', widget, data):
        keys = data.value.keys()
        for index in range(len(keys)):
            value_name = '{}{}.value'.format(base_name, index)
            extracted[keys[index]] = request[value_name]
        return extracted
    index = 0
    while True:
        key_name = '{}{}.key'.format(base_name, index)
        value_name = '{}{}.value'.format(base_name, index)
        if key_name in request:
            key = request[key_name].strip()
            if key:
                extracted[key] = request[value_name]
            index += 1
            continue
        break
    return extracted


@managedprops('key_type', 'value_type')
def dict_datatype_extractor(widget, data):
    extracted = data.extracted
    if extracted is UNSET:
        return extracted
    key_type = widget.attrs['key_type']
    value_type = widget.attrs['value_type']
    if key_type is UNSET and value_type is UNSET:
        return extracted
    typed_extracted = odict()
    for key, value in extracted.items():
        if key_type is not UNSET:
            try:
                key = key_type(key)
            except (ValueError, UnicodeEncodeError, UnicodeDecodeError):
                datatype_label = DATATYPE_LABELS.get(key_type)
                raise ExtractionError(_(
                    'dict_key_type_mismatch',
                    default=u'Key ${key} is not a valid ${datatype}.',
                    mapping={
                        'key': key,
                        'datatype': datatype_label
                    }
                ))
        if value_type is not UNSET:
            try:
                value = value_type(value)
            except (ValueError, UnicodeEncodeError, UnicodeDecodeError):
                datatype_label = DATATYPE_LABELS.get(value_type)
                raise ExtractionError(_(
                    'dict_value_type_mismatch',
                    default=u'Value ${value} is not a valid ${datatype}.',
                    mapping={
                        'value': value,
                        'datatype': datatype_label
                    }
                ))
        typed_extracted[key] = value
    return typed_extracted


@managedprops('static', 'required')
def static_dict_required_extractor(widget, data):
    extracted = data.extracted
    if extracted is UNSET:
        return extracted
    required = attr_value('required', widget, data)
    if not (required and attr_value('static', widget, data)):
        return extracted
    for value in extracted.values():
        if value:
            continue
        if isinstance(required, STR_TYPE):
            raise ExtractionError(required)
        raise ExtractionError(_(
            'dict_values_required',
            default='Dict values must not be empty'
        ))
    return extracted


factory.register(
    'dict',
    extractors=[
        dict_extractor,
        static_dict_required_extractor,
        dict_datatype_extractor,
        generic_required_extractor
    ],
    edit_renderers=[
        dict_edit_renderer,
        compound_renderer
    ],
    display_renderers=[
        dict_display_renderer
    ],
)

factory.doc['blueprint']['dict'] = """\
Add-on widget `yafowil.widget.dict
<http://github.com/conestack/yafowil.widget.dict/>`_.
"""

factory.defaults['dict.default'] = odict()

factory.defaults['dict.error_class'] = 'error'

factory.defaults['dict.message_class'] = 'errormessage'

factory.defaults['dict.table_class'] = 'dictwidget'
factory.doc['props']['dict.table_class'] = """\
CSS classes rendered on dict table.
"""

factory.defaults['dict.key_class'] = 'keyfield'
factory.doc['props']['dict.key_class'] = """\
CSS classes rendered on key input fields.
"""

factory.defaults['dict.value_class'] = 'valuefield'
factory.doc['props']['dict.value_class'] = """\
CSS classes rendered on value input fields.
"""

factory.defaults['dict.key_label'] = UNSET
factory.doc['props']['dict.key_label'] = """\
Label for dict keys column.
"""

factory.defaults['dict.value_label'] = UNSET
factory.doc['props']['dict.value_label'] = """\
Label for dict values column.
"""

factory.defaults['dict.key_type'] = UNSET
factory.doc['props']['dict.key_type'] = """\
Datatype for dict keys.
"""

factory.defaults['dict.value_type'] = UNSET
factory.doc['props']['dict.value_type'] = """\
Datatype for dict values.
"""

factory.defaults['dict.head'] = {}
factory.doc['props']['dict.head'] = """\
B/C Labels for dict keys and values columns. Expect a dict containing
``key`` and ``value`` keys.
"""

factory.defaults['dict.static'] = False
factory.doc['props']['dict.static'] = """\
Flag whether dict is immutable.
"""

factory.defaults['dict.scrollable'] = False
factory.doc['props']['dict.scrollable'] = """\
Flag whether to render scrollbar for large widgets on smaller viewports.
Depends on yafowil.widget.scrollbar.
"""
