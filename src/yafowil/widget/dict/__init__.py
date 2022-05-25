from yafowil.base import factory
from yafowil.utils import entry_point
import os
import webresource as wr


resources_dir = os.path.join(os.path.dirname(__file__), 'resources')


##############################################################################
# Common
##############################################################################

# webresource ################################################################

scripts = wr.ResourceGroup(
    name='yafowil-dict-scripts',
    path='yafowil.widget.dict'
)
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

default_styles = wr.ResourceGroup(
    name='yafowil-dict-styles',
    path='yafowil.widget.dict'
)
default_styles.add(wr.StyleResource(
    name='yafowil-dict-css',
    directory=os.path.join(resources_dir, 'default'),
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

bootstrap_styles = wr.ResourceGroup(
    name='yafowil-dict-styles',
    path='yafowil.widget.dict'
)
bootstrap_styles.add(wr.StyleResource(
    name='yafowil-dict-css',
    directory=os.path.join(resources_dir, 'bootstrap'),
    resource='widget.css'
))

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

plone5_styles = wr.ResourceGroup(
    name='yafowil-dict-styles',
    path='yafowil.widget.dict'
)
plone5_styles.add(wr.StyleResource(
    name='yafowil-dict-css',
    directory=os.path.join(resources_dir, 'plone5'),
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

    # Default
    factory.register_theme(
        'default', 'yafowil.widget.dict', resources_dir,
        js=js, css=default_css
    )
    factory.register_scripts('default', 'yafowil.widget.dict', scripts)
    factory.register_styles('default', 'yafowil.widget.dict', default_styles)

    # Bootstrap
    factory.register_theme(
        ['bootstrap', 'bootstrap3'], 'yafowil.widget.dict', resources_dir,
        js=js, css=bootstrap_css
    )
    factory.register_scripts(
        ['bootstrap', 'bootstrap3'],
        'yafowil.widget.dict',
        scripts
    )
    factory.register_styles(
        ['bootstrap', 'bootstrap3'],
        'yafowil.widget.dict',
        bootstrap_styles
    )

    # Plone 5
    factory.register_theme(
        'plone5', 'yafowil.widget.dict', resources_dir,
        js=js, css=plone5_css
    )
    factory.register_scripts('plone5', 'yafowil.widget.dict', scripts)
    factory.register_styles('plone5', 'yafowil.widget.dict', plone5_styles)
