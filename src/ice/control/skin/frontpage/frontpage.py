### -*- coding: utf-8 -*- ####################################################
#
#  Copyright (C) 2010 Ilshad R. Khabibullin <astoon.net at gmail.com>
#
#  This library is free software: you can redistribute it and/or modify it
#  under the terms of the GNU General Public License as published by the Free
#  Software Foundation, either version 3 of the License.
#
#  This software is distributed in the hope that it will be useful, but
#  WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
#  or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
#  for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this software.  If not, see <http://www.gnu.org/licenses/>.
#
#  Project homepage: <http://launchpad.net/ice.control>
#
##############################################################################

from urllib import quote
from zope.authentication.interfaces import IUnauthenticatedPrincipal
from zope.traversing.browser.absoluteurl import absoluteURL
from zope.security import checkPermission

class Pagelet:
    
    def update(self):
        self.unauth = IUnauthenticatedPrincipal.providedBy(self.request.principal)
        self.context_url = absoluteURL(self.context, self.request)
        self.request_url = quote(self.request.getURL())
        self.is_admin = checkPermission('zope.ManageServices', self.context)
