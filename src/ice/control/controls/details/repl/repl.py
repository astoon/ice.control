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

from zope.component import getUtility
from zope.session.interfaces import ISession
from zope.traversing.browser.absoluteurl import absoluteURL
from ice.control.repl.interfaces import IDispatcher

PREFIX = 'ice.control.repl.'

class REPL:

    def session_data(self):
        session = ISession(self.request)
        absolute_url = absoluteURL(self.context, self.request)
        return session[PREFIX + absolute_url]

    def get_repl(self):
        dispatcher = getUtility(IDispatcher)
        data = self.session_data()

        try:
            credentials = data['id'], data['password']
        except KeyError:
            credentials = dispatcher.set_session(self.context)
            data['id'], data['password'] = credentials

        return dispatcher.get_session(*credentials)

    def plugins_names(self):
        return self.repl().get_plugins().keys()

    def clear(self):
        dispatcher = getUtility(IDispatcher)
        data = self.session_data()
        try:
            dispatcher.del_session(data['id'], data['password'])
        except KeyError:
            pass

    def interact(self):
        code = self.request.get('code')
        repl = self.get_repl()
