#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import mock
import os
import sys

sys.path.insert(0, os.path.abspath('../..'))
# -- General configuration ------------------------------------------------
#
# import mock, sys
# MOCK_MODULES = ['typeguard']
# for mod_name in MOCK_MODULES:
#     sys.modules[mod_name] = mock.Mock()

extensions = ['sphinx.ext.autodoc', 'sphinx.ext.autosummary']


templates_path = ['_templates']

source_suffix = '.rst'

master_doc = 'index'

project = 'yacargo'
copyright = '2020, Pasha Yegorov'
author = 'Pasha Yegorov'

from yacargo import constants

version = constants.VERSION
release = ''

language = 'ru'
exclude_patterns = ['_build']
pygments_style = 'sphinx'

todo_include_todos = True

html_theme = 'alabaster'
# html_theme_options = {}
html_static_path = ['_static']

# This is required for the alabaster theme
# refs: http://alabaster.readthedocs.io/en/latest/installation.html#sidebars
html_sidebars = {
    'index': ['sidebarintro.html', 'sourcelink.html', 'searchbox.html',
              'hacks.html'],
    '**': [
        # 'relations.html',  # needs 'show_related': True theme option to display
        # 'searchbox.html',
    ]
}

htmlhelp_basename = 'yacargodoc'

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    #
    # 'papersize': 'letterpaper',

    # The font size ('10pt', '11pt' or '12pt').
    #
    # 'pointsize': '10pt',

    # Additional stuff for the LaTeX preamble.
    #
    # 'preamble': '',

    # Latex figure (float) alignment
    #
    # 'figure_align': 'htbp',
}

latex_documents = [
    (master_doc, 'yacargo.tex', 'yacargo Documentation',
     'Pavel Yegorov', 'manual'),
]

man_pages = [
    (master_doc, 'yacargo', 'yacargo Documentation',
     [author], 1)
]
texinfo_documents = [
    (master_doc, 'yacargo', 'yacargo Documentation',
     author, 'yacargo', 'One line description of project.',
     'Miscellaneous'),
]
