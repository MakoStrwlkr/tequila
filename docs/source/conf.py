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
from recommonmark.parser import CommonMarkParser
import sphinx_bootstrap_theme

sys.path.insert(0, os.path.abspath('../src'))


# -- Project information -----------------------------------------------------

project = 'tequila'
copyright = '2019, Jakob S. Kottmann, Sumner Alperin-Lea, Teresa Tamayo, Cyrille Lavigne, Abhinav Anand, Maha Kesebi'
author = 'Jakob S. Kottmann, Sumner Alperin-Lea, Teresa Tamayo, Cyrille Lavigne, Abhinav Anand, Maha Kesebi'

# The full version, including alpha/beta/rc tags
release = 'XXXXX'


# -- General configuration ---------------------------------------------------

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = 'en'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
# Activate the theme.
html_theme = 'bootstrap'
html_theme_path = sphinx_bootstrap_theme.get_html_theme_path()

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

extensions = ['sphinx.ext.napoleon','recommonmark','sphinx.ext.autodoc','sphinx.ext.autosummary'] ## For docstring syntax 
source_suffix = ['.rst']


napoleon_google_docstring = True
napoleon_use_param = False
napoleon_use_ivar = True

pdf_documents = [('index', u'rst2pdf', u'Sample rst2pdf doc', u'tequila documentation'),]

### Theme oprtions

html_theme_options = {
    # Navigation bar title. (Default: ``project`` value)
    'navbar_title': 'Tequila',

    # Tab name for entire site. (Default: "Site")
    'navbar_site_name': 'Documentation',

    # A list of tuples containing pages or urls to link to.
    # Valid tuples should be in the following forms:
    #    (name, page)                 # a link to a page
    #    (name, "/aa/bb", 1)          # a link to an arbitrary relative url
    #    (name, "http://example.com", True) # arbitrary absolute url
    # Note the "1" or "True" value above as the third argument to indicate
    # an arbitrary url.
    'navbar_links': [
         ("Overview", "https://github.com/aspuru-guzik-group/tequila/blob/master/docs/tequila.pdf"),
         ("Installation", "Intallation", True),
         ("GitHub", "https://github.com/aspuru-guzik-group/tequila", True),
    ],

    # Render the next and previous page links in navbar. (Default: true)
    'navbar_sidebarrel': True,

    # Render the current pages TOC in the navbar. (Default: true)
    'navbar_pagenav': True,

    # Location of link to source.
    # Options are "nav" (default), "footer" or anything else to exclude.
    'source_link_position': 'none',

    # Bootswatch (https://bootswatch.com/) theme.
    'bootswatch_theme': 'Sandstone',

    # Choose Bootstrap version.
    # Values: "3" (default) or "2" (in quotes)
    'bootstrap_version': '3',
}
