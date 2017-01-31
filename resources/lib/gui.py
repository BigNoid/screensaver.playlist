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

import xbmc
import xbmcgui
import xbmcaddon

ADDON = xbmcaddon.Addon()
ADDON_VERSION = ADDON.getAddonInfo('version')
ADDON_NAME = ADDON.getAddonInfo('name')
ADDON_LANGUAGE = ADDON.getLocalizedString
ADDON_ICON = ADDON.getAddonInfo('icon')


class Screensaver(xbmcgui.WindowXMLDialog):
    '''Function play_playlist: Load video playlist (.m3u or .xsp) and shuffle if needed
       Function stop_playlist: Clear playlist
    '''
    def __init__(self, *args, **kwargs):
        pass

    def onInit(self):
        self.stop = False
        self._get_settings()
        self.monitor = PlaylistMonitor(action=self.stop_playlist)
        self.player = PlaylistPlayer(action=self.stop_playlist)
        self.play_playlist()

    def _get_settings(self):
        self.playlist_path = ADDON.getSetting("playlist")
        self.random = ADDON.getSetting("random")

    def stop_playlist(self):
        self.stop = True
        self.player.stop()
        playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playlist.clear()
        self.close()
        xbmc.log(msg='%s: Playback stopped' % (ADDON_NAME), level=xbmc.LOGDEBUG)

    def play_playlist(self):
        if self.playlist_path.endswith('.m3u'):
            queue = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
            queue.load(self.playlist_path)
            if self.random:
                queue.shuffle()
            valid_playlist = True
        elif self.playlist_path.endswith('.xsp'):
            queue = self.playlist_path
            valid_playlist = True
        else:
            xbmc.executebuiltin('Notification(%s, %s, %s, %s)' % (ADDON_NAME, ADDON_LANGUAGE(30003), 5000, ADDON_ICON))
            valid_playlist = False
        if valid_playlist:
            self.player.play(queue, windowed=True)
            while not self.monitor.abortRequested() and not self.stop:
                if self.monitor.waitForAbort(1):
                    break


class PlaylistPlayer(xbmc.Player):
    '''Implementation of xbmc.Player'''
    def __init__(self, *args, **kwargs):
        xbmc.log(msg='%s: Playback started' % (ADDON_NAME), level=xbmc.LOGDEBUG)
        xbmc.Player.__init__(self)
        self.action = kwargs['action']

    def onPlayBackStopped(self):
        self.action()


class PlaylistMonitor(xbmc.Monitor):
    '''Implementation of xbmc.Monitor'''
    def __init__(self, *args, **kwargs):
        self.action = kwargs['action']

    def onScreensaverDeactivated(self):
        if not xbmc.Player().isPlayingVideo():
            self.action()
