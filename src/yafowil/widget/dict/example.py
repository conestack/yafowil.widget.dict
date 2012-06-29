from odict import odict
from yafowil.base import factory


DOC_MUTABLE_DICT = """
Mutable Dict
------------

Dict where key/value pairs can be added, deleted and sorted.

.. code-block:: python

    value = odict()
    value['foo'] = 'Foo'
    value['bar'] = 'Bar'
    dict = factory('#field:dict', value=value, props={
        'label': 'Fill the dict',
        'required': 'At least one entry is required',
        'head': {'key': 'Key', 'value': 'Value'}})
"""

def mutable_dict():
    form = factory('fieldset', name='yafowil.widget.dict.mutable_dict')
    value = odict()
    value['foo'] = 'Foo'
    value['bar'] = 'Bar'
    form['dict'] = factory('#field:dict', value=value, props={
        'label': 'Fill the dict',
        'required': 'At least one entry is required',
        'head': {'key': 'Key', 'value': 'Value'}})
    return {'widget': form,
            'doc': DOC_MUTABLE_DICT,
            'title': 'Mutable Dict'}


DOC_IMMUTABLE_DICT = """
Immutable Dict
--------------

Dict where only values can be edited.

.. code-block:: python

    value = odict()
    value['baz'] = 'Baz'
    value['bam'] = 'Bam'
    dict = factory('#field:dict', value=value, props={
        'label': 'Modify the dict',
        'required': 'No Empty values allowed',
        'static': True,
        'head': {'key': 'Key', 'value': 'Value'}})
"""

def immutable_dict():
    form = factory('fieldset', name='yafowil.widget.dict.immutable_dict')
    value = odict()
    value['baz'] = 'Baz'
    value['bam'] = 'Bam'
    form['dict'] = factory('#field:dict', value=value, props={
        'label': 'Modify the dict',
        'required': 'No Empty values allowed',
        'static': True,
        'head': {'key': 'Key', 'value': 'Value'}})
    return {'widget': form,
            'doc': DOC_IMMUTABLE_DICT,
            'title': 'Imutable Dict'}


def get_example():
    return [
        mutable_dict(),
        immutable_dict(),
    ]