"""Sphinx ReadTheDocs theme.

From https://github.com/ryan-roemer/sphinx-bootstrap-theme.

"""
from os import path
from sphinx_rtd_theme import directives
from sphinx_rtd_theme.extensions import latex_mods

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
    return [
#        path.join(cur_dir, 'sphinx_rtd_theme', 'texinputs', 'openwide.sty'),
        path.join(cur_dir, 'sphinx_rtd_theme', 'texinputs', 'rtdsphinx.sty'),
        path.join(cur_dir, 'sphinx_rtd_theme', 'texinputs', 'rtdsphinxhowto.cls'),
        path.join(cur_dir, 'sphinx_rtd_theme', 'texinputs', 'rtdsphinxmanual.cls')
    ]

def setup(app):
    directives.setup(app)
    
    app.config.html_logo = path.join(get_html_theme_path(), 'sphinx_rtd_theme', "static", "images", "logo_html.png")
    app.config.latex_logo = path.join(get_html_theme_path(), 'sphinx_rtd_theme', "static", "images", "logo_latex.png")
    app.config.html_favicon = path.join(get_html_theme_path(), 'sphinx_rtd_theme', "static", "images", "favicon.png")
    
    app.config.latex_additional_files = get_latex_theme_files()
    
