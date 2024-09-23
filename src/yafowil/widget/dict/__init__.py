from yafowil.base import factory
from yafowil.utils import entry_point
import os
import webresource as wr


resources_dir = os.path.join(os.path.dirname(__file__), 'resources')


##############################################################################
# Common
##############################################################################

# webresource ################################################################

dict_js = wr.ScriptResource(
    name='yafowil-dict-js',
    depends='jquery-js',
    resource='default/widget.js',
    compressed='widget.min.js'
)

# B/C resources ##############################################################

js = [{
    'group': 'yafowil.widget.dict.common',
    'resource': 'default/widget.js',
    'order': 20,
}]


##############################################################################
# Default
##############################################################################

# webresource ################################################################

default_resources = wr.ResourceGroup(
    name='yafowil.widget.dict',
    directory=resources_dir,
    path='yafowil-dict'
)
default_resources.add(dict_js)
default_resources.add(wr.StyleResource(
    name='yafowil-dict-css',
    directory=os.path.join(resources_dir, 'default'),
    path='yafowil-dict/default',
    resource='widget.css'
))

# B/C resources ##############################################################

default_css = [{
    'group': 'yafowil.widget.dict.common',
    'resource': 'default/widget.css',
    'order': 20,
}]


##############################################################################
# Bootstrap
##############################################################################

# webresource ################################################################

bootstrap_resources = wr.ResourceGroup(
    name='yafowil.widget.dict',
    directory=resources_dir,
    path='yafowil-dict'
)
bootstrap_resources.add(dict_js)
bootstrap_resources.add(wr.StyleResource(
    name='yafowil-dict-css',
    directory=os.path.join(resources_dir, 'bootstrap'),
    path='yafowil-dict/bootstrap',
    resource='widget.css'
))

# B/C resources ##############################################################

bootstrap_css = [{
    'group': 'yafowil.widget.dict.common',
    'resource': 'bootstrap/widget.css',
    'order': 20,
}]


##############################################################################
# Bootstrap 5
##############################################################################

# webresource ################################################################
bootstrap5_js = wr.ScriptResource(
    name='yafowil-dict-js',
    depends='jquery-js',
    resource='bootstrap5/widget.js',
    compressed='bootstrap5/widget.min.js'
)
bootstrap5_resources = wr.ResourceGroup(
    name='yafowil.widget.dict',
    directory=resources_dir,
    path='yafowil-dict'
)
bootstrap5_resources.add(bootstrap5_js)
bootstrap5_resources.add(wr.StyleResource(
    name='yafowil-dict-css',
    directory=os.path.join(resources_dir, 'bootstrap5'),
    path='yafowil-dict/bootstrap5',
    resource='widget.css'
))

# B/C resources ##############################################################

bootstrap5_css = [{
    'group': 'yafowil.widget.dict.common',
    'resource': 'bootstrap5/widget.css',
    'order': 20,
}]


##############################################################################
# Plone5
##############################################################################

# webresource ################################################################

plone5_resources = wr.ResourceGroup(
    name='yafowil.widget.dict',
    directory=resources_dir,
    path='yafowil-dict'
)
plone5_resources.add(dict_js)
plone5_resources.add(wr.StyleResource(
    name='yafowil-dict-css',
    directory=os.path.join(resources_dir, 'plone5'),
    path='yafowil-dict/plone5',
    resource='widget.css'
))

# B/C resources ##############################################################

plone5_css = [{
    'group': 'yafowil.widget.dict.common',
    'resource': 'plone5/widget.css',
    'order': 20,
}]


##############################################################################
# Registration
##############################################################################

@entry_point(order=10)
def register():
    import yafowil.widget.dict.widget  # noqa

    widget_name = 'yafowil.widget.dict'

    # Default
    factory.register_theme(
        'default',
        widget_name,
        resources_dir,
        js=js,
        css=default_css
    )
    factory.register_resources('default', widget_name, default_resources)

    # Bootstrap
    factory.register_theme(
        ['bootstrap', 'bootstrap3'],
        widget_name,
        resources_dir,
        js=js,
        css=bootstrap_css
    )
    factory.register_resources(
        ['bootstrap', 'bootstrap3'],
        widget_name,
        bootstrap_resources
    )

    # Bootstrap 5
    factory.register_theme(
        ['bootstrap5'],
        widget_name,
        resources_dir,
        js=bootstrap5_js,
        css=bootstrap5_css
    )
    factory.register_resources(
        ['bootstrap5'],
        widget_name,
        bootstrap5_resources
    )

    # Plone 5
    factory.register_theme(
        'plone5',
        widget_name,
        resources_dir,
        js=js,
        css=plone5_css
    )
    factory.register_resources('plone5', widget_name, plone5_resources)
