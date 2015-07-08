#
# awesome.py
#
#    https://gist.github.com/tk0miya/8558c915187442a0f7dd
#    
#   Author: @tk0miya
#   License: Apache 2.0
#
from docutils import nodes, utils
 
 
def awesome_role(name, rawtext, text, lineno, inliner, options={}, content=[]):
    awesome_tag = '<i class="fa fa-%s"></i>' % utils.unescape(text)
    raw = nodes.raw('', awesome_tag, format='html')
    return [raw], []
 
 
def setup(app):
    app.add_role('awesome', awesome_role)
    app.add_stylesheet('http://maxcdn.bootstrapcdn.com/font-awesome/4.1.0/css/font-awesome.min.css')