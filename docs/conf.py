# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Kubernetes Test App'
copyright = '2024, Yin-Chi Chan'
author = 'Yin-Chi Chan'
version = '0.1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'myst_parser',
    'sphinxcontrib.kroki',
    'sphinx_copybutton',
    'sphinx_rtd_dark_mode'
]

myst_enable_extensions = [
    "attrs_inline",
    "attrs_block",
    "colon_fence",
    "smartquotes",
    "strikethrough",
    "tasklist",
]


templates_path = ['_templates']
exclude_patterns = ['.venv']


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_context = {
    'display_github': True,
    'github_user': 'yinchi',
    'github_repo': 'k8s-demo',
    'github_version': 'main',
    'conf_py_path': '/docs/'
}
html_static_path = ['_static']
html_css_files = ['custom.css']