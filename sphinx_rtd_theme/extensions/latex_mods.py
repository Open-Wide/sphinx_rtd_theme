# -*- coding: utf-8 -*-
from docutils import nodes
from docutils.frontend import OptionParser
from docutils.io import FileOutput
import os
import sphinx.builders.latex
from sphinx.locale import _
import locale
locale.setlocale(locale.LC_TIME,'')
import time
from sphinx.util.console import bold
from sphinx.util.osutil import copyfile
from sphinx.util.smartypants import educate_quotes_latex
from sphinx.util.texescape import tex_escape_map
import sphinx.writers.latex
from sphinx.writers.latex import LaTeXWriter

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
        self.elements['usepackages'] += "\n" + '\usepackage[table]{xcolor}'
        self.elements['usepackages'] += "\n" + '\usepackage{tcolorbox}'
        
        if builder.config.today:
            self.elements['date'] = builder.config.today
        else:
            self.elements['date'] = time.strftime(builder.config.today_fmt or _('%B %d, %Y'))

    def format_docclass(self, docclass):
        """ prepends prefix to sphinx document classes
        """
        if docclass in self.docclasses:
            docclass = 'rtdsphinx' + docclass
        return docclass

    def depart_table(self, node):
        if self.table.rowcount > 30:
            self.table.longtable = True
        self.body = self._body
        if not self.table.longtable:
            self.body.append('\\begin{table}[ht]\n')
            self.body.append('\\centering\n')
        if not self.table.longtable and self.table.caption is not None:
            self.body.append(u'\n\n\\begin{threeparttable}\n'
                             u'\\capstart\\caption{%s}\n' % self.table.caption)
            for id in self.next_table_ids:
                self.body.append(self.hypertarget(id, anchor=False))
            if node['ids']:
                self.body.append(self.hypertarget(node['ids'][0], anchor=False))
            self.next_table_ids.clear()
        if self.table.longtable:
            self.body.append('\n\\begin{longtable}')
            endmacro = '\\end{longtable}\n\n'
        elif self.table.has_verbatim:
            self.body.append('\n\\begin{tabular}')
            endmacro = '\\end{tabular}\n\n'
        elif self.table.has_problematic and not self.table.colspec:
            # if the user has given us tabularcolumns, accept them and use
            # tabulary nevertheless
            self.body.append('\n\\begin{tabular}')
            endmacro = '\\end{tabular}\n\n'
        else:
            self.body.append('\n\\begin{tabulary}{\\linewidth}')
            endmacro = '\\end{tabulary}\n\n'
        if self.table.colspec:
            self.body.append(self.table.colspec)
        else:
            if self.table.has_problematic:
                colwidth = 0.95 / self.table.colcount
                colspec = ('p{%.3f\\linewidth}|' % colwidth) * \
                    self.table.colcount
                self.body.append('{|' + colspec + '}\n')
            elif self.table.longtable:
                self.body.append('{|' + ('l|' * self.table.colcount) + '}\n')
            else:
                self.body.append('{|' + ('L|' * self.table.colcount) + '}\n')
        if self.table.longtable and self.table.caption is not None:
            self.body.append(u'\\caption{%s}' % self.table.caption)
            for id in self.next_table_ids:
                self.body.append(self.hypertarget(id, anchor=False))
            self.next_table_ids.clear()
            self.body.append(u'\\\\\n')
        if self.table.longtable:
            self.body.append('\\hline\n')
            self.body.extend(self.tableheaders)
            self.body.append('\\endfirsthead\n\n')
            self.body.append(r'\hline \multicolumn{%s}{|r|}{{\textsf{%s}}} \\ \hline'
                             % (self.table.colcount,
                             _('continued from previous page')))
            self.body.append('\n\\hline\n')
            self.body.extend(self.tableheaders)
            self.body.append('\\endhead\n\n')
            self.body.append(r'\hline \multicolumn{%s}{|r|}{{\textsf{%s}}} \\ \hline'
                             % (self.table.colcount,
                             _('Continued on next page')))
            self.body.append('\n\\endfoot\n\n')
            self.body.append('\\endlastfoot\n\n')
        else:
            self.body.append('\\hline\n')
            self.body.extend(self.tableheaders)
        self.body.extend(self.tablebody)
        self.body.append(endmacro)
        if not self.table.longtable and self.table.caption is not None:
            self.body.append('\\end{threeparttable}\n\n')
        if not self.table.longtable:
            self.body.append('\\end{table}\n\n')
        self.table = None
        self.tablebody = None

    def visit_row(self, node):
        BaseTranslator.visit_row(self, node)
        if isinstance(node.parent, nodes.thead):
            self.body.append('\\headcol ')

    def visit_entry(self, node):
        if self.table.col == 0:
            while self.remember_multirow.get(self.table.col + 1, 0):
                self.table.col += 1
                self.remember_multirow[self.table.col] -= 1
                if self.remember_multirowcol.get(self.table.col, 0):
                    extracols = self.remember_multirowcol[self.table.col]
                    self.body.append(' \multicolumn{')
                    self.body.append(str(extracols + 1))
                    self.body.append('}{|l|}{}')
                    self.table.col += extracols
                self.body.append(' & ')
        else:
            self.body.append(' & ')
        self.table.col += 1
        context = ''
        if 'morecols' in node:
            self.body.append(' \multicolumn{')
            self.body.append(str(node.get('morecols') + 1))
            if self.table.col == 1:
                self.body.append('}{|l|}{')
            else:
                self.body.append('}{l|}{')
            context += '}'
        if 'morerows' in node:
            self.body.append(' \multirow{')
            self.body.append(str(node.get('morerows') + 1))
            self.body.append('}{*}{')
            context += '}'
            self.remember_multirow[self.table.col] = node.get('morerows')
        if 'morecols' in node:
            if 'morerows' in node:
                self.remember_multirowcol[self.table.col] = node.get('morecols')
            self.table.col += node.get('morecols')
        if isinstance(node.parent.parent, nodes.thead):
            self.body.append('\\textsf{\\relax\\textcolor{white}{')
            context += '}}'
        while self.remember_multirow.get(self.table.col + 1, 0):
            self.table.col += 1
            self.remember_multirow[self.table.col] -= 1
            context += ' & '
            if self.remember_multirowcol.get(self.table.col, 0):
                extracols = self.remember_multirowcol[self.table.col]
                context += ' \multicolumn{'
                context += str(extracols + 1)
                context += '}{l|}{}'
                self.table.col += extracols
        self.context.append(context)

    def visit_topic(self, node):
        self.body.append('\\begin{tcolorbox}\n'
                         '\\begin{minipage}{0.95\\linewidth}\n')

    def depart_topic(self, node):
        self.body.append('\\end{minipage}\n'
                         '\\end{tcolorbox}\n')
    visit_sidebar = visit_topic
    depart_sidebar = depart_topic

sphinx.writers.latex.LaTeXTranslator = LaTeXRTDTranslator