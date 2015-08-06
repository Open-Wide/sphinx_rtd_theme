# -*- coding: utf-8 -*-

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
 
 
def awesome_role(name, rawtext, text, lineno, inliner, options={}, content=[]):
    awesome_tag = '<i class="fa fa-%s"></i>' % utils.unescape(text)
    raw = nodes.raw('', awesome_tag, format='html')
    return [raw], []

def clear_role(name, rawtext, text, lineno, inliner, options={}, content=[]):
    clear_both_tag = '<div class="clear-%s"></div>' % utils.unescape(text)
    raw = nodes.raw('', clear_both_tag, format='html')
    return [raw], []
 
 
def setup(app):
    app.add_role('tag', tag_role)
    app.add_stylesheet('css/tag.css')
    
    app.add_role('awesome', awesome_role)
    app.add_stylesheet('http://maxcdn.bootstrapcdn.com/font-awesome/4.3.0/css/font-awesome.min.css')
    
    app.add_role('clear', clear_role)
    app.add_stylesheet('css/clear.css')