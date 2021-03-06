#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys

sys.path.insert(0, os.path.abspath('../..'))
from yacargo import __version__

extensions = ['sphinx.ext.autodoc', 'sphinx.ext.autosummary', "sphinx_rtd_theme"]

templates_path = ['_templates']

source_suffix = '.rst'

master_doc = 'index'

project = 'yacargo'
copyright = '2020, Pasha Yegorov'
author = 'Pasha Yegorov'

version = __version__
release = ''

language = 'ru'
exclude_patterns = ['_build']
pygments_style = 'sphinx'

todo_include_todos = True

html_theme = "sphinx_rtd_theme"
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

man_pages = [
    (master_doc, 'yacargo', 'yacargo Documentation',
     [author], 1)
]
