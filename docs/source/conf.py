# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import sphinx_rtd_theme
import sys


project = 'OptFALT'
copyright = '2024, Burlakov Yuri, Kohanova Vlada, Kuzmin Vyacheslav'
author = 'Burlakov Yuri, Kohanova Vlada, Kuzmin Vyacheslav'
release = '1.0.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ["sphinx_rtd_theme",
    'sphinx.ext.autodoc',
    'sphinx.ext.coverage',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode']

napoleon_google_docstring = False
napoleon_use_param = False
napoleon_use_ivar = True
html_theme = "sphinx_rtd_theme"

templates_path = ['_templates']
exclude_patterns = []

language = 'en'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_static_path = ['_static']

# -- Autodoc section ---------------------------------------------------------

sys.path.insert(0, "/home/crucian/Desktop/aerokittes/Yura_s/OptFALT/")
# Disable prepending module names
add_module_names = False
# Sort members by type
autodoc_member_order = 'groupwise'
# Document __init__, __repr__, and __str__ methods
def skip(app, what, name, obj, would_skip, options):
    if name in ("__init__", "__repr__", "__str__"):
        return False
    return would_skip
def setup(app):
    app.connect("autodoc-skip-member", skip)
