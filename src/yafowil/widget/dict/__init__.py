import os
from yafowil.base import factory


resourcedir = os.path.join(os.path.dirname(__file__), 'resources')

js = [{
    'resource': 'widget.js',
    'thirdparty': False,
    'order': 20,
}]

default_css = [{
    'resource': 'default/widget.css',
    'thirdparty': False,
    'order': 20,
}]

bootstrap_css = [{
    'resource': 'bootstrap/widget.css',
    'thirdparty': False,
    'order': 20,
}]


def register():
    import widget
    factory.register_theme('default', 'yafowil.widget.dict',
                           resourcedir, js=js, css=default_css)
    factory.register_theme('bootstrap', 'yafowil.widget.dict',
                           resourcedir, js=js, css=bootstrap_css)