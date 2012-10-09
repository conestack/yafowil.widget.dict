from odict import odict
from yafowil.base import (
    UNSET,
    factory,
    ExtractionError,
    fetch_value
)
from yafowil.compound import (
    compound_extractor,
    compound_renderer,
)
from yafowil.utils import (
    managedprops,
    css_managed_props,
)

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
            icon = tag('i', '&#160;', class_=ICON_CSS[key])
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
    table = widget['table'] = factory('table', props={
                                      'structural': True,
                                      'class': widget.attrs['table_class']})
    head = table['head'] = factory('thead', props={'structural': True})
    row = head['row'] = factory('tr', props={'structural': True})
    row['key'] = factory('th', props={
        'structural': True,
        'label': widget.attrs['head']['key']})
    row['value'] = factory('th', props={
        'structural': True,
        'label': widget.attrs['head']['value']})
    if not widget.attrs['static']:
        row['actions'] = factory('th:dict_actions', props={
            'structural': True,
            'add': True})
    table['body'] = factory('tbody', props={'structural': True})


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
        k_props = {'class': 'key'}
        if static:
            k_props['disabled'] = 'disabled'
        row['key'] = factory('td:text', value=key, name='key', props=k_props)
        row['value'] = factory('td:text', value=val, name='value', props={
            'class': 'value'})
        if not static:
            row['actions'] = factory('td:dict_actions', props={
                'add': True,
                'remove': True,
                'up': True,
                'down': True})
        i += 1


def raise_extraction_error(widget):
    if isinstance(widget.attrs['required'], basestring):
        raise ExtractionError(widget.attrs['required'])
    raise ExtractionError(widget.attrs['required_message'])


def extract_static(data, basename):
    request = data.request
    ret = odict()
    index = 0
    keys = data.value.keys()
    while True:
        valuename = '%s%i.value' % (basename, index)
        if request.has_key(valuename):
            if index >= len(keys):
                raise ExtractionError('invalid number of static values')
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
        if request.has_key(keyname):
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
    if widget.attrs.get('required'):
        if ret is UNSET:
            raise_extraction_error(widget)
        if static:
            for val in ret.values():
                if not val:
                    raise_extraction_error(widget)
    return ret


def dict_display_renderer(widget, data):
    value = data.value
    if not value:
        value = dict()
    values = list()
    for key, val in value.items():
        values.append(data.tag('dt', key) + data.tag('dd', val))
    head = u''
    if widget.attrs.get('head'):
        head = '%s: %s' % (widget.attrs['head']['key'],
                           widget.attrs['head']['value'])
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

factory.defaults['dict.static'] = False
"""Flag whether dict is immutable.
"""
factory.doc['props']['dict.static'] = \
"""Makes keys immutable.
"""
