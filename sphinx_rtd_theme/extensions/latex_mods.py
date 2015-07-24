# -*- coding: utf-8 -*-
import os

from docutils.io import FileOutput
from docutils.frontend import OptionParser
from docutils import nodes

import sphinx.builders.latex
from sphinx.util.smartypants import educate_quotes_latex
from sphinx.writers.latex import LaTeXWriter
from sphinx.util.console import bold
from sphinx.util.osutil import copyfile
from sphinx.util.texescape import tex_escape_map
import sphinx.writers.latex

# remove usepackage for sphinx here, we add it later in the preamble in conf.py
sphinx.writers.latex.HEADER = sphinx.writers.latex.HEADER.replace('\usepackage{sphinx}', '\usepackage{openwide_sphinx}')
sphinx.writers.latex.HEADER = sphinx.writers.latex.HEADER.replace('%(makeindex)s', '\pagestyle{fancy}\n%(makeindex)s')
#
BaseTranslator = sphinx.writers.latex.LaTeXTranslator

class LaTeXRTDTranslator(BaseTranslator):

    def __init__(self, document, builder):
        BaseTranslator.__init__(self, document, builder)
        if builder.config.language and builder.config.language != 'ja':
            self.elements['fncychap'] = '\\usepackage[Bjornstrup]{fncychap}'

sphinx.writers.latex.LaTeXTranslator = LaTeXRTDTranslator

#class CustomLaTeXTranslator(LaTeXRTDTranslator):
#    def astext(self):
#            return (#HEADER % self.elements +
#                    #self.highlighter.get_stylesheet() +
#                    u''.join(self.body)
#                    #'\n' + self.elements['footer'] + '\n' +
#                    #self.generate_indices() +
#                    #FOOTER % self.elements
#                    )
#
#    def unknown_departure(self, node):
#        if node.tagname == 'only':
#            return
#        return super(CustomLaTeXTranslator, self).unknown_departure(node)
#
#    def unknown_visit(self, node):
#        if node.tagname == 'only':
#            return
#        return super(CustomLaTeXTranslator, self).unknown_visit(node)
    
#class CustomLaTeXBuilder(sphinx.builders.latex.LaTeXBuilder):
#
#    def write(self, *ignored):
#        super(CustomLaTeXBuilder, self).write(*ignored)
#
#        backup_translator = sphinx.writers.latex.LaTeXTranslator
#        sphinx.writers.latex.LaTeXTranslator = CustomLaTeXTranslator
#        backup_doc = sphinx.writers.latex.BEGIN_DOC
#        sphinx.writers.latex.BEGIN_DOC = ''
#
#        # output these as include files
#        
#        sphinx.writers.latex.LaTeXTranslator = backup_translator
#        sphinx.writers.latex.BEGIN_DOC = backup_doc
#
#    def finish(self, *args, **kwargs):
#        super(CustomLaTeXBuilder, self).finish(*args, **kwargs)
#
## monkey patch the shit out of it
#sphinx.builders.latex.LaTeXBuilder = CustomLaTeXBuilder