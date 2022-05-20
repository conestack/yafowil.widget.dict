from yafowil.base import factory
from yafowil.utils import entry_point
import os
import webresource as wr


resources_dir = os.path.join(os.path.dirname(__file__), 'resources')


##############################################################################
# Common
##############################################################################

# webresource ################################################################

scripts = wr.ResourceGroup(name='scripts')
scripts.add(wr.ScriptResource(
    name='yafowil-dict-js',
    depends='jquery-js',
    directory=resources_dir,
    resource='widget.js',
    compressed='widget.min.js'
))

# B/C resources ##############################################################

js = [{
    'group': 'yafowil.widget.dict.common',
    'resource': 'widget.js',
    'order': 20,
}]


##############################################################################
# Default
##############################################################################

# webresource ################################################################

default_styles = wr.ResourceGroup(name='styles')
default_styles.add(wr.StyleResource(
    name='yafowil-dict-css',
    directory=os.path.join(resources_dir, 'default'),
    resource='widget.css'
))

default_resources = wr.ResourceGroup(name='dict-resources')
default_resources.add(scripts)
default_resources.add(default_styles)

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

bootstrap_styles = wr.ResourceGroup(name='styles')
bootstrap_styles.add(wr.StyleResource(
    name='yafowil-dict-css',
    directory=os.path.join(resources_dir, 'bootstrap'),
    resource='widget.css'
))

bootstrap_resources = wr.ResourceGroup(name='dict-resources')
bootstrap_resources.add(scripts)
bootstrap_resources.add(bootstrap_styles)

# B/C resources ##############################################################

bootstrap_css = [{
    'group': 'yafowil.widget.dict.common',
    'resource': 'bootstrap/widget.css',
    'order': 20,
}]


##############################################################################
# Plone5
##############################################################################

# webresource ################################################################

plone5_styles = wr.ResourceGroup(name='styles')
plone5_styles.add(wr.StyleResource(
    name='yafowil-dict-css',
    directory=os.path.join(resources_dir, 'plone5'),
    resource='widget.css'
))

plone5_resources = wr.ResourceGroup(name='dict-resources')
plone5_resources.add(scripts)
plone5_resources.add(plone5_styles)

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

    # Default
    factory.register_theme(
        'default', 'yafowil.widget.dict', resources_dir,
        js=js, css=default_css, resources=default_resources
    )
    # Bootstrap
    factory.register_theme(
        'bootstrap', 'yafowil.widget.dict', resources_dir,
        js=js, css=bootstrap_css, resources=bootstrap_resources
    )
    # Plone 5
    factory.register_theme(
        'plone5', 'yafowil.widget.dict', resources_dir,
        js=js, css=plone5_css, resources=plone5_resources
    )
