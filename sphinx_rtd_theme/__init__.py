"""Sphinx ReadTheDocs theme.

From https://github.com/ryan-roemer/sphinx-bootstrap-theme.

"""
from os import path
from sphinx_rtd_theme import directives

VERSION = (0, 1, 8)

__version__ = ".".join(str(v) for v in VERSION)
__version_full__ = __version__
    

def get_html_theme_path():
    """Return list of HTML theme paths."""
    cur_dir = path.abspath(path.dirname(path.dirname(__file__)))
    return cur_dir
    

def get_latex_theme_files():
    """Return list of HTML theme paths."""
    cur_dir = path.abspath(path.dirname(path.dirname(__file__)))
    return [path.join(cur_dir, 'sphinx_rtd_theme', 'texinputs','openwide.sty')]

def setup(app):
    directives.setup(app)
