import os
from yafowil.base import factory


resourcedir = os.path.join(os.path.dirname(__file__), 'resources')

js = [{
    'resource': 'widget.js',
    'thirdparty': False,
    'order': 20,
}]

css = [{
    'resource': 'widget.css',
    'thirdparty': False,
    'order': 20,
}]


def register():
    import widget
    factory.register_theme('default', 'yafowil.widget.dict',
                           resourcedir, js=js, css=css)


###############################################################################
# XXX: outdated below
###############################################################################

def get_resource_dir():
    return resourcedir


def get_js():
    return js


def get_css():
    return css
