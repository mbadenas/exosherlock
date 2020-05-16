# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from recommonmark.parser import CommonMarkParser

import exosherlock

class CustomCommonMarkParser(CommonMarkParser):
    def visit_document(self, node):
        pass

# -- Project information -----------------------------------------------------

project = 'exosherlock'
copyright = '2020, Mariona Badenas-Agusti, Oriol Abril-Pla'
author = 'Mariona Badenas-Agusti, Oriol Abril-Pla'

# The full version, including alpha/beta/rc tags
version = exosherlock.__version__
release = version

master_doc = "index"

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.doctest",
    "sphinx.ext.coverage",
    "sphinx.ext.intersphinx",
    "sphinx.ext.autosummary",
    "sphinx.ext.viewcode",
    "sphinx.ext.githubpages",
    "numpydoc",
    "nbsphinx",
    "IPython.sphinxext.ipython_directive",
    "IPython.sphinxext.ipython_console_highlighting",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'pyramid'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# ipython directive configuration
ipython_warning_is_error = False

# Generate API documentation when building
autosummary_generate = True
numpydoc_show_class_members = False

source_suffix = [".rst", ".md"]

# A shorter title for the navigation bar.  Default is the same as html_title.
html_short_title = "exosherlock"


# The name of an image file (relative to this directory)
html_logo = "logo/logo.png"


# The name of an image file (relative to this directory) to use as a favicon
html_favicon = "logo/favicon.ico"

def setup(app):
    app.add_source_suffix('.md', 'markdown')
    app.add_source_parser(CustomCommonMarkParser)

# Example configuration for intersphinx
intersphinx_mapping = {
    "pandas": ("https://pandas.pydata.org/docs/", None),
}
