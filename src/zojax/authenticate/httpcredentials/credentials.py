##############################################################################
#
# Copyright (c) 2007 Zope Corporation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""

$Id$
"""
from zope import interface
from zope.app.security.interfaces import ILoginPassword
from zope.app.container.contained import Contained
from persistent import Persistent

from zojax.authentication.interfaces import ICredentialsPlugin, ICredentialsUpdater, ISimpleCredentials
from zojax.authentication.credentials import SimpleCredentials
from zojax.authentication.factory import CredentialsPluginFactory
from zojax.authentication.authentication import cache

_ = lambda x: x

class HTTPCredentialsPlugin(Persistent, Contained):
    interface.implements(ICredentialsPlugin, ICredentialsUpdater)

    _v_credentials = None

    def extractCredentials(self, request):
        global cache
        if cache.defaultcreds is not None:
            creds, temp = cache.defaultcreds
            if temp:
                cache.defaultcreds = None
            return creds
        else:
            a = ILoginPassword(request, None)
            if a is not None:
                login, password = a.getLogin(), a.getPassword()
                if login is not None and password is not None:
                    return SimpleCredentials(login, password)

    def updateCredentials(self, request, creds, temp=False):
        if ISimpleCredentials.providedBy(creds):
            global cache
            cache.defaultcreds = (creds, temp)


factory = CredentialsPluginFactory(
    'http.credentials', HTTPCredentialsPlugin, (),
    _(u'HTTP Basic credentials plugin'), _(u'Extract credentials from HTTP Header.'))
