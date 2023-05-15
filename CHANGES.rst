Changes
=======

2.0a1 (2023-05-15)
------------------

- Add ``webresource`` support.
  [rnix]

- Extend JS by ``dict_on_array_add`` and ``register_array_subscribers``
  functions to enable usage in ``yafowil.widget.array``.
  [lenadax]

- Add support for key and value datatypes.
  [rnix]

- Rewrite JavaScript using ES6.
  [rnix]

- Remove B/C property callback tests. Property callbacks always
  gets passed ``widget`` and ``data`` as of yafowil 3.0.0.
  [rnix]


1.8 (2020-07-09)
----------------

- Fix re-rendering of widget if values required but empty dict passed.
  [rnix]

- Remove ``dict_builder``. Entire widget is rendered now in ``dict_renderer``
  [rnix]

- General code cleanup and modernization.
  [rnix]


1.7 (2018-07-16)
----------------

- Python 3 compatibility.
  [rnix]

- Convert doctests to unittests.
  [rnix]

- Add ``key_label`` and ``value_label`` blueprint properties. They replace
  ``head`` dict property containing ``key`` and ``value``. Needed to make i18n
  work when using dict blueprint in in yaml forms. ``head`` still works for
  B/C reasons.
  [rnix]


1.6 (2016-09-09)
----------------

- Use ``$.closest()`` for acquiring dict widget wrapper table
  when adding row.
  [rnix, 2016-06-28]

- Add dedicated CSS for ``plone5`` theme provided by ``yafowil.plone``.
  [rnix, 2016-06-28]

- Use ``yafowil.utils.entry_point`` decorator.
  [rnix, 2016-06-27]

- Minor bootstrap theme CSS changes.
  [rnix, 2016-06-27]


1.5 (2015-01-23)
----------------

- Bootstrap 3 compatibility.
  [rnix, 2014-08-06]

- Introduce ``key_class`` and ``value_class`` properties which gets rendered
  to corresponding input fields.
  [rnix, 2014-08-06]


1.4
---

- Add translations, package depends now ``yafowil`` >= 2.1
  [rnix, 2014-04-30]


1.3.1
-----

- use ``yafowil.utils.attr_value`` wherever possible.
  [rnix, 2012-10-25]


1.3
---

- Adopt resource providing
  [rnix, 2012-06-12]

- Remove example app
  [rnix, 2012-06-12]


1.2
---

- make ready for YAFOWIL 1.3
  [agitator, 2012-02-19]


1.1.1
-----

- add dict binder function to ``yafowil.widget.array`` hooks if found
  [rnix, 2011-10-05]


1.1
---

- adopt to yafowil 1.2
  [jensens, 2011-09-20]

- make ready for z3c.autoinclude+Plone (only if available).
  [jensens, 2011-09-20]


1.0.2
-----

- be gentle and display an error if for some reason a static dict is feeded
  with additional values.
  [jensens - 2011-09-01]


1.0.1
-----

- make conditional resource registration more general for Zope2 available.
  [jensens, 2011-08-26]


1.0
---

- add display renderer
  [rnix, 2011-08-04]

- adopt to yafowil 1.1
  [rnix, 2011-07-08]

- adopt tests for form novalidate property
  [rnix, 2011-05-23]


0.9.1
-----

- test coverage
  [rnix, 2011-05-07]

- python 2.4 fix
  [chaoflow, 2011-03-01]


0.9
---

- made it work [rnix]
