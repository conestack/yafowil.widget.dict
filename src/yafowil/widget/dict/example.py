from yafowil import loader
from yafowil.base import factory

def get_example():
    part = factory(u'fieldset', name='yafowilwidgetdict')
    part['dict'] = factory(
        'field:label:error:dict',
        name='mydict',
        props={
            'label': 'Fill the dict',
            'head': {'key': 'Key', 'value': 'Value'}})
    return [{'widget': part, 'doc': ''}]
