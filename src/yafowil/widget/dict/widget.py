from odict import odict
from yafowil.base import (
    UNSET,
    factory,
    ExtractionError,
)
from yafowil.compound import (
    compound_extractor,
    compound_renderer,
)
from yafowil.common import _value
from yafowil.utils import tag

def actions_renderer(widget, data):
    actions = list()
    for key in ['add', 'remove', 'up', 'down']:
        if widget.attrs.get(key):
            class_ = 'dict_row_%s' % key
            action = tag('a', '&nbsp;', href='#', class_=class_)
            actions.append(action)
    return tag('div', *actions, class_='dict_actions')

factory.register('dict_actions',
                 [],
                 [actions_renderer])

def dict_builder(widget, factory):
    table = widget['table'] = factory(
        'table',
        props={
            'structural': True,
            'class': 'dictwidget',
        })
    head = table['head'] = factory('thead', props={'structural': True})
    row = head['row'] = factory('tr', props={'structural': True})
    row['key'] = factory(
        'th',
        props = {
            'structural': True,
            'label': widget.attrs['head']['key'],
        })
    row['value'] = factory(
        'th',
        props={
            'structural': True,
            'label': widget.attrs['head']['value'],
        })
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
    table = widget['table']
    table.attrs['id'] = 'dictwidget_%s.entry' % widget.dottedpath
    body = table['body']
    body.clear()
    value = _value(widget, data)
    if not value:
        return
    i = 0
    for key, val in value.items():
        row = body['entry%i' % i] = factory('tr')
        if not widget.attrs['static']:
            row['key'] = factory(
                'td:text',
                value = key,
                name = 'key',
                props = {
                    'class': 'key',
                })
        else:
            row['key'] = factory(
                'td:text',
                value = key,
                name = 'key',
                props = {
                    'class': 'key',
                    #'disabled': 'disabled',
                })
        row['value'] = factory(
            'td:text',
            value = val,
            name = 'value',
            props = {
                'class': 'value',
            })
        if not widget.attrs['static']:
            row['actions'] = factory(
                'td:dict_actions',
                props = {
                    'add': True,
                    'remove': True,
                    'up': True,
                    'down': True,
                })
        i += 1

def raise_extraction_error(widget):
    if isinstance(widget.attrs['required'], basestring):
        raise ExtractionError(widget.attrs['required'])
    raise ExtractionError(widget.attrs['required_message'])

def dict_extractor(widget, data):
    ret = odict()
    body = widget['table']['body']
    basename = '%s.entry' % body.dottedpath
    req = data.request
    index = 0
    while True:
        keyname = '%s%i.key' % (basename, index)
        valuename = '%s%i.value' % (basename, index)
        if data.request.has_key(keyname):
            key = req[keyname].strip()
            if key:
                ret[key] = req[valuename]
            index += 1
            continue
        break
    if len(ret) == 0:
        ret = UNSET
    if widget.attrs.get('required'):
        if ret is UNSET:
            raise_extraction_error(widget)
        if widget.attrs['static']:
            for val in ret.values():
                if not val:
                    raise_extraction_error(widget)
    return ret

factory.defaults['dict.default'] = odict()
factory.defaults['dict.static'] = False
factory.defaults['dict.error_class'] = 'error'
factory.defaults['dict.message_class'] = 'errormessage'
factory.register('dict',
                 [compound_extractor, dict_extractor],
                 [dict_renderer, compound_renderer],
                 [],
                 [dict_builder])