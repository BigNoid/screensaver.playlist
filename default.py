#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#     Copyright (C) 2017 BigNoid
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program. If not, see <http://www.gnu.org/licenses/>.

import os
import sys
import xbmc
import xbmcaddon


ADDON = xbmcaddon.Addon()
ADDONID = ADDON.getAddonInfo('id')
ADDON_VERSION = ADDON.getAddonInfo('version')
CWD = ADDON.getAddonInfo('path').decode("utf-8")
ADDON_NAME = ADDON.getAddonInfo('name')
ADDON_LANGUAGE = ADDON.getLocalizedString
ADDON_ICON = ADDON.getAddonInfo('icon')
ADDON_RESOURCE = xbmc.translatePath(os.path.join(CWD, 'resources', 'lib').encode("utf-8")).decode("utf-8")


sys.path.append(ADDON_RESOURCE)

xbmc.log(msg='%s version %s started' % (ADDON_NAME, ADDON_VERSION), level=xbmc.LOGDEBUG)
if (__name__ == "__main__"):
    import gui
    screensaver_gui = gui.Screensaver('screensaver-playlist.xml', CWD, 'default')
    screensaver_gui.doModal()
    del screensaver_gui
xbmc.log(msg='%s version %s stopped' % (ADDON_NAME, ADDON_VERSION), level=xbmc.LOGDEBUG)
