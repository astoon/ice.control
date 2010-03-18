### -*- coding: utf-8 -*- ####################################################
#
#  Copyright (C) 2010 Ilshad R. Khabibullin <astoon.net at gmail.com>
#
#  This library is free software: you can redistribute it and/or modify it
#  under the terms of the GNU General Public License as published by the Free
#  Software Foundation, either version 3 of the License.
#
#  This library is distributed in the hope that it will be useful, but
#  WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
#  or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
#  for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from zope.interface import implements, Interface
from zope.component import adapts, queryMultiAdapter
from zope.dublincore.interfaces import IZopeDublinCore
from zope.traversing.browser.absoluteurl import absoluteURL
from zope.interface.common.mapping import IEnumerableMapping
from zope.publisher.interfaces.browser import IBrowserRequest
from zope.container.interfaces import IReadContainer
from zope.location.interfaces import ILocationInfo
from zope.size.interfaces import ISized
from interfaces import IXML, ICONS, XMLDOC, XMLNODE

class XMLBase(object):
    implements(IXML)
    adapts(Interface, IBrowserRequest)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def name(self):
        # This method is filter
        try:
            return ILocationInfo(self.context).getName()
        except TypeError:
            return u''

    def path(self):
        # This method is common and it needn't to be reimplement
        # in subclasses in standard situations.
        return absoluteURL(self.context, self.request) or u''

    def title(self):
        # Sometimes you need to reimplement this method in subclass,
        # mostly if an object does not uses Dublin Core metadata
        try:
            title = IZopeDublinCore(self.context).title
            if title:
                return u'[ ' + title + ' ]'
        except TypeError:
            pass
        return u''

    def icon_url(self):
        # This method needn't to reimplement never. Define icon for
        # new content type using special zcml directive
        icon = queryMultiAdapter((self.context, self.request), name=ICONS)
        if icon:
            return icon.url()
        return u''

    def is_container(self):
        # I recommend reimplement this and return IS_CONTAINER
        # or empty string directly
        return IReadContainer.providedBy(self.context) or u''

    def size(self):
        # This is common pattern. If you have defined adapter to ISized
        # then you needn't to reimplement this method in subclasses.
        try:
            return ISized(self.context).sizeForDisplay()
        except TypeError:
            return u''

    def length(self):
        # I strongly recommend to reimplement this in your subclass
        try:
            enumerable = IEnumerableMapping(self.context)
        except TypeError:
            return u''
        return len(enumerable)

    def sort_key(self):
        # Reimplement if you like sort this item within its
        # parent container
        return None

    def to_xml(self):
        # You needn't reimplement this never in your life, man
        return XMLNODE % (self.name(), self.path() + u"/", self.title(),
                          self.icon_url(), self.size(), self.length(),
                          self.is_container() and u'true' or u'false')

    def node_xmldoc(self):
        return XMLDOC % self.to_xml()

    def children_xmldoc(self):
        # If you need custom filter then reimplement this method.
        # Otherwise this implementation is generic and it is correct
        # for standard cases.
        try:
            rc = IReadContainer(self.context)
        except TypeError:
            return XMLDOC % u''
        specs = [queryMultiAdapter((value, self.request), IXML)
                for value in rc.values()]
        specs = filter(lambda x:x, specs)
        specs.sort(key = lambda x: x.sort_key())
        nodes = [x.to_xml() for x in specs]
        return XMLDOC % u'\n'.join(nodes)
