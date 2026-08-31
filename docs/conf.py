# Configuration file for the Sphinx documentation builder.
import os
import sys

project = 'Omni View Business Command Centre (Review Fork)'
copyright = '2026, Harisfazillah Jamel (linuxmalaysia)'
author = 'Harisfazillah Jamel'
release = '1.0.0'

extensions = [
    'myst_parser',
]

source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown',
}

master_doc = 'SUMMARY'
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
html_theme = 'sphinx_rtd_theme'
