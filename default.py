#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#     Copyright (C) 2016 Team-Kodi
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

import xbmc
import xbmcaddon

ADDON = xbmcaddon.Addon()
ADDON_VERSION = ADDON.getAddonInfo('version')
ADDON_NAME = ADDON.getAddonInfo('name')
ADDON_LANGUAGE = ADDON.getLocalizedString
ADDON_ICON = ADDON.getAddonInfo('icon')


def log(txt):
    message = '%s: %s' % (ADDON_NAME, txt.encode('ascii', 'ignore'))
    xbmc.log(msg=message, level=xbmc.LOGDEBUG)


class Main:
    def __init__(self):
        self.playlistplayer = PlaylistPlayer()
        playlist = ADDON.getSetting("playlist")
        random = ADDON.getSetting("random")
        if playlist.endswith('.m3u'):
            queue = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
            queue.load(playlist)
            if random:
                queue.shuffle()
            xbmc.Player().play(queue)
            while xbmc.getCondVisibility("Player.HasMedia"):
                xbmc.sleep(1000)
        elif playlist.endswith('.xsp'):
            xbmc.Player().play(playlist)
            while xbmc.getCondVisibility("Player.HasMedia"):
                xbmc.sleep(1000)
        else:
            xbmc.executebuiltin('Notification(%s, %s, %d, %s)' % (ADDON_NAME, ADDON_LANGUAGE(30003), 5000, ADDON_ICON))


class PlaylistPlayer(xbmc.Player):
    def __init__(self):
        xbmc.log(msg='Playlist Screensaver started', level=xbmc.LOGDEBUG)

    def onPlaybackEnded(self):
        Main()

    def onPlayBackStopped(self):
        playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playlist.clear()
        xbmc.log(msg='Playlist Screensaver stopped', level=xbmc.LOGDEBUG)


log('script version %s started' % ADDON_VERSION)
Main()
log('script version %s stopped' % ADDON_VERSION)
