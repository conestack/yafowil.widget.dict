from yafowil.base import factory
from yafowil.compound import compound_renderer
from yafowil.utils import tag

def actions_renderer(widget, data):
    return tag('a', '&nbsp;', href='', class_='add_dict_row')

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
        }
    )
    table['body'] = factory('tbody', props={'structural': True})

def dict_extractor(widget, data):
    pass

def dict_renderer(widget, data):
    pass
    #widget['table']['row1'] = factory('tr',
    #                                  props={'structural': True})
    #widget['table']['row1']['field1'] = factory('td:text', name='field1')

factory.register('dict',
                 [dict_extractor],
                 [dict_renderer, compound_renderer],
                 [],
                 [dict_builder])