from yafowil.base import factory

def dict_extractor(widget, data):
    pass

def dict_renderer(widget, data):
    pass

factory.register('dict',
                 [dict_extractor],
                 [dict_renderer])