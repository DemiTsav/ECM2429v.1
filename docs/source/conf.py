import os
import sys
sys.path.insert(0, os.path.abspath('../../'))

project = 'Fleet Management System'
copyright = '2025, 730095122'
author = '730095122'
release = '1'

templates_path = ['_templates']
exclude_patterns = []

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
plantuml = 'plantuml'


extensions = [
    'sphinx.ext.graphviz',
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinxcontrib.mermaid'
    ]
