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

def actions_renderer(widget, data):
    tag = data.tag
    actions = list()
    for key in ['add', 'remove', 'up', 'down']:
        if widget.attrs.get(key):
            class_ = 'dict_row_%s' % key
            action = tag('a', '&#160;', href='#', class_=class_)
            actions.append(action)
    return tag('div', *actions, class_='dict_actions')

factory.doc['widget']['dict_actions'] = UNSET # dont document internal widget
factory.register('dict_actions',
                 [],
                 [actions_renderer])

def dict_builder(widget, factory):
    table = widget['table'] = factory(
        'table',
        props={
            'structural': True,
            'class': 'dictwidget',
        }
    )
    head = table['head'] = factory('thead', props={'structural': True})
    row = head['row'] = factory('tr', props={'structural': True})
    row['key'] = factory(
        'th',
        props = {
            'structural': True,
            'label': widget.attrs['head']['key'],
        }
    )
    row['value'] = factory(
        'th',
        props={
            'structural': True,
            'label': widget.attrs['head']['value'],
        }
    )
    if not widget.attrs['static']:
        row['actions'] = factory(
            'th:dict_actions',
            props = {
                'structural': True,
                'add': True,
            }
        )
    table['body'] = factory('tbody', props={'structural': True})

def dict_renderer(widget, data):
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
        row['key'] = factory(
            'td:text',
            value = key,
            name = 'key',
            props = k_props,
        )
        row['value'] = factory(
            'td:text',
            value = val,
            name = 'value',
            props = {
                'class': 'value',
            },
        )
        if not static:
            row['actions'] = factory(
                'td:dict_actions',
                props = {
                    'add': True,
                    'remove': True,
                    'up': True,
                    'down': True,
                },
            )
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

def dict_extractor(widget, data):
    static = widget.attrs['static']
    body = widget['table']['body']
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

factory.doc['widget']['dict'] = \
"""Add-on widget `yafowil.widget.dict 
<http://github.com/bluedynamics/yafowil.widget.dict/>`_.
"""

factory.defaults['dict.default'] = odict()
factory.defaults['dict.static'] = False
factory.defaults['dict.error_class'] = 'error'
factory.defaults['dict.message_class'] = 'errormessage'
factory.register('dict',
                 [compound_extractor, dict_extractor],
                 [dict_renderer, compound_renderer],
                 [],
                 [dict_builder])