from yafowil.base import factory
from yafowil.compound import compound_renderer
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
    widget.clear()
    table = widget['table'] = factory('table', props={'structural': True})
    head = table['head'] = factory('thead')
    row = head['row'] = factory('tr')
    row['key'] = factory(
        'th',
        props = {
            'label': widget.attrs['head']['key'],
        })
    row['value'] = factory(
        'th',
        props={
            'label': widget.attrs['head']['value'],
        })
    row['actions'] = factory(
        'th:dict_actions',
        props = {
            'add': True,
        }
    )
    table['body'] = factory('tbody', props={'structural': True})

def dict_extractor(widget, data):
    pass

def dict_renderer(widget, data):
    body = widget['table']['body']
    value = _value(widget, data)
    if not value:
        return
    i = 0
    for key, val in value.items():
        row = body['entry%i' % i] = factory('tr')
        row['key'] = factory(
            'td:text',
            value = key,
            name = 'key')
        row['value'] = factory(
            'td:text',
            value = val,
            name = 'value')
        row['actions'] = factory(
            'td:dict_actions',
            props = {
                'add': True,
                'remove': True,
                'up': True,
                'down': True,
            })
        i += 1

factory.register('dict',
                 [dict_extractor],
                 [dict_renderer, compound_renderer],
                 [],
                 [dict_builder])