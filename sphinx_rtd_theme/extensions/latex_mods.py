## -*- coding: utf-8 -*-
#
from os import path
import locale
locale.setlocale(locale.LC_TIME,'')
import time
from docutils import nodes
from sphinx.locale import _
from sphinx.util.osutil import copyfile
from sphinx import addnodes
import sphinx.builders.latex
import sphinx.writers.latex
import sphinx.config
#
# remove usepackage for sphinx here, we add it later in the preamble in conf.py
sphinx.writers.latex.HEADER = sphinx.writers.latex.HEADER.replace('\\usepackage{sphinx}', '\\usepackage{rtdsphinx}')
sphinx.writers.latex.HEADER = sphinx.writers.latex.HEADER.replace('%(makeindex)s', '\pagestyle{fancy}\n%(makeindex)s')
sphinx.writers.latex.HEADER = sphinx.writers.latex.HEADER.replace('%(makeindex)s', '\\newcommand{\\rtdbackgroundimage}{%(backgroundimage)s}\n%(makeindex)s')
sphinx.writers.latex.HEADER = sphinx.writers.latex.HEADER.replace('%(makeindex)s', '\\newcommand{\\rtdheaderbackgroundimage}{%(headerbackgroundimage)s}\n%(makeindex)s')
sphinx.writers.latex.HEADER = sphinx.writers.latex.HEADER.replace('%(makeindex)s', '\\newcommand{\\rtdsubtitle}{%(subtitle)s}\n%(makeindex)s')
sphinx.writers.latex.HEADER = sphinx.writers.latex.HEADER.replace('%(makeindex)s', '\\newcommand{\\rtdreference}{%(reference)s}\n%(makeindex)s')
sphinx.writers.latex.HEADER = sphinx.writers.latex.HEADER.replace('%(makeindex)s', '\\newcommand{\\rtdcopyright}{%(copyright)s}\n%(makeindex)s')
sphinx.writers.latex.HEADER = sphinx.writers.latex.HEADER.replace('%(makeindex)s', '\\newcommand{\\rtdfooterimage}{%(footerimage)s}\n%(makeindex)s')

BaseTranslator = sphinx.writers.latex.LaTeXTranslator

class LaTeXRTDTranslator(BaseTranslator):
    
    default_elements = BaseTranslator.default_elements
    
#    default_elements['maketitle'] = '\pagestyle{firstpage}\n\\maketitle\n\pagestyle{normal}'
    default_elements['maketitle'] = '\\maketitle'
    default_elements['shorthandoff'] = '\\pagenumbering{arabic}'
    default_elements['backgroundimage'] = ''
    default_elements['headerbackgroundimage'] = ''
    default_elements['subtitle'] = ''
    default_elements['reference'] = ''
    default_elements['copyright'] = ''
    
    def __init__(self, document, builder):
        BaseTranslator.__init__(self, document, builder)
        if builder.config.language:
            if builder.config.language != 'ja':
                self.elements['fncychap'] = '\\usepackage[Bjornstrup]{fncychap}'
            if builder.config.language == 'fr':
                self.elements['babel'] = '\\usepackage[cyr]{aeguill}\n\\usepackage[francais]{babel}'
        
        if builder.config.today:
            self.elements['date'] = builder.config.today
        else:
            self.elements['date'] = time.strftime(builder.config.today_fmt or _('%B %d, %Y')).decode('utf-8')

        if builder.config.latex_background_image:
            self.elements['backgroundimage'] = u'\includegraphics[width=19cm]{%s}' % path.basename(builder.config.latex_background_image)

        if builder.config.latex_header_background_image:
            self.elements['headerbackgroundimage'] = u'\includegraphics[width=19cm]{%s}' % path.basename(builder.config.latex_header_background_image)

        if builder.config.latex_footer_image:
            self.elements['footerimage'] = u'\includegraphics[width=7cm]{%s}' % path.basename(builder.config.latex_footer_image)
            
        if builder.config.latex_logo:
            self.elements['logo'] = '\\includegraphics[height=3cm]{%s}\\par' % \
                                    path.basename(builder.config.latex_logo)

        if builder.config.subtitle:
            self.elements['subtitle'] = path.basename(builder.config.subtitle)

        if builder.config.reference:
            self.elements['reference'] = u'{%s}' % builder.config.reference

        if builder.config.copyright:
            self.elements['copyright'] = u'{%s}' % builder.config.copyright
                                    
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
            self.body.append('\\begin{table}[H]\n')
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

BaseBuilder= sphinx.builders.latex.LaTeXBuilder

class LaTeXRTDBuilder(BaseBuilder):
    def finish(self):
        BaseBuilder.finish(self)

        # the backbround is handled differently
        if self.config.latex_background_image:
            backgroundbase = path.basename(self.config.latex_background_image)
            copyfile(path.join(self.confdir, self.config.latex_background_image),
                     path.join(self.outdir, backgroundbase))
        self.info('done')

        # the footer is handled differently
        if self.config.latex_footer_image:
            footerbase = path.basename(self.config.latex_footer_image)
            copyfile(path.join(self.confdir, self.config.latex_footer_image),
                     path.join(self.outdir, footerbase))
        self.info('done')

        # the header is handled differently
        if self.config.latex_footer_image:
            headerbase = path.basename(self.config.latex_header_background_image)
            copyfile(path.join(self.confdir, self.config.latex_header_background_image),
                     path.join(self.outdir, headerbase))
        self.info('done')

sphinx.builders.latex.LaTeXBuilder = LaTeXRTDBuilder