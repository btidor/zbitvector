"""
Configuration file for the Sphinx documentation builder.

For the full list of built-in configuration values, see the documentation:
https://www.sphinx-doc.org/en/master/usage/configuration.html
"""

project = "zbitvector"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.intersphinx",
]

templates_path = ["_templates"]
exclude_patterns = []


html_theme = "alabaster"
html_static_path = ["_static"]
html_css_files = ["custom.css"]

html_sidebars = {"**": ["sidebar.html", "relations.html"]}
html_theme_options = {
    "show_powered_by": False,
}
html_show_copyright = False
html_show_sourcelink = False

autodoc_default_options = {
    "members": True,
    "special-members": True,
    "exclude-members": "__hash__, __init__, __repr__, __weakref__",
    "member-order": "bysource",
    "show-inheritance": True,
}
intersphinx_mapping = {"python": ("https://docs.python.org/3", None)}


import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
