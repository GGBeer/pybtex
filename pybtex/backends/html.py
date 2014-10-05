# vim: fileencoding=utf-8

# Copyright (c) 2008, 2009, 2010, 2011, 2012  Andrey Golovizin
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from pybtex.backends import BaseBackend
import pybtex.io


PROLOGUE = u"""<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN">
<html>
<head><meta name="generator" content="Pybtex">
<meta http-equiv="Content-Type" content="text/html; charset=%s">
<title>Bibliography</title>
</head>
<body>
<dl>
"""

class Backend(BaseBackend):
    u"""
    >>> from pybtex.richtext import Text, Tag, Symbol
    >>> print Tag('em', Text(u'Л.:', Symbol('nbsp'), u'<<Химия>>')).render(Backend())
    <em>Л.:&nbsp;&lt;&lt;Химия&gt;&gt;</em>

    """

    default_suffix = u'.html'

    def __init__(self, encoding=None):
        super(Backend, self).__init__(encoding=encoding)
        self.symbols[u'ndash']    = u'&ndash;'
        self.symbols[u'newblock'] = u'\n'
        self.symbols[u'nbsp']     = u'&nbsp;'

    def format_str(self, text):
        #encoding = self.encoding or pybtex.io.get_default_encoding()
        #return text.encode(encoding, 'xmlcharrefreplace')
        text = text.replace(u"&", u"&amp;")
        text = text.replace(u">", u"&gt;")
        text = text.replace(u"<", u"&lt;")
        return text

    def format_tag(self, tag, text):
        return ur'<%s>%s</%s>' % (tag, text, tag)

    def format_href(self, url, text):
        return ur'<a href="%s">%s</a>' % (url, text)

    def write_prologue(self):
        encoding = self.encoding or pybtex.io.get_default_encoding()
        self.output(PROLOGUE % encoding)

    def write_epilogue(self):
        self.output(u'</dl></body></html>\n')

    def write_entry(self, key, label, text):
        self.output(u'<dt>%s</dt>\n' % label)
        self.output(u'<dd>%s</dd>\n' % text)
