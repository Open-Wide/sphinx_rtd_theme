#
# tags.py
#
#    https://gist.github.com/tk0miya/8558c915187442a0f7dd
#    
#   Author: @tk0miya
#   License: Apache 2.0
#
from docutils import nodes, utils
import re
 
 
def tag_role(name, rawtext, text, lineno, inliner, options={}, content=[]):
    tag_class = 'default'
    tag_text = utils.unescape(text)
    tag_array = tag_text.split('::')
    # @type tag_array a
    if len(tag_array) == 2:
        if tag_array[0]:
            tag_class = tag_array[0]
        tag_content = tag_array[1]
    else:
        tag_content = tag_array[0]
        
    tag_tag = '<span class="tag tag-%s">%s</span>' % (tag_class, tag_content)
    raw = nodes.raw('', tag_tag, format='html')
    return [raw], []
 
 
def setup(app):
    app.add_role('tag', tag_role)
    app.add_stylesheet('css/tag.css')