"""
Configuration file for the Sphinx documentation builder.

For the full list of built-in configuration values, see the documentation:
https://www.sphinx-doc.org/en/master/usage/configuration.html
"""

project = "zbitvector"
release = "1.0b1"


extensions = []

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
