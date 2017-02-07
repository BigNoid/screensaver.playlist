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
        self.repeat = xbmc.getLocalizedString(591)
        self._get_settings()
        self.player = xbmc.Player()
        self.play_playlist()

    def _get_settings(self):
        self.playlist_path = ADDON.getSetting("playlist")
        self.random = ADDON.getSetting("random")

    def stop_playlist(self):
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
            # play windowed, skin xml has fullscreen videowindow control.
            self.player.play(queue, windowed=True)
            # save value of playlist repeat
            self.repeat = xbmc.getInfoLabel("Playlist.Repeat(video)")
            # sleep for 1 sec to allow infolabel to save before setting to repeat all
            xbmc.sleep(1000)
            # set playlist to repeat for infinite playback
            xbmc.executebuiltin("PlayerControl(RepeatAll)")

    def onAction(self, action):
        # catch all actions and stop the screensaver
        if action.getId():
            # restore value of playlist repeat
            if self.repeat == xbmc.getLocalizedString(592):
                xbmc.executebuiltin("PlayerControl(RepeatOne)")
            elif self.repeat == xbmc.getLocalizedString(591):
                xbmc.executebuiltin("PlayerControl(RepeatOff)")
            self.stop_playlist()
