from __future__ import division

__author__ = "David"

from random import shuffle
import os
import json
import subprocess
import xbmc
import xbmcgui
from io import open
from resources.config import config

def generate_playlist():
    videos = list(())

    with open(config["video_prefs_path"], encoding="utf-8") as videos_file:
        videos_json = json.load(videos_file)
    
    uploader_count = len(videos_json["uploaders"])
    uploaders_processed = 0
    
    progress_bar = xbmcgui.DialogProgress()
    progress_bar.create("Generating Playlist")

    for uploader in videos_json["uploaders"]:
        for playlist in videos_json["uploaders"][uploader]["playlists"]:
            for video in videos_json["uploaders"][uploader]["playlists"][playlist]["videos"]:
                videos.append([video["title"], "plugin://plugin.video.youtube/play/?video_id=" + video["id"]])
        
        uploaders_processed += 1
        progress_bar.update(int(100 * uploaders_processed / uploader_count))
    
    progress_bar.close()

    return videos


def play_videos():
    videos = generate_playlist()

    shuffle(videos)
    
    playlist_file = "#EXTM3U\n"

    for i in range(len(videos)):
        playlist_file += "#EXTINF:0," + videos[i][0] + "\n"
        playlist_file += videos[i][1] + "\n"

    playlist_out = open(config["playlist_file_path"], "w", encoding="utf-8")
    playlist_out.write(playlist_file)
    playlist_out.close()
    
    xbmc.Player().play(config["playlist_file_path"])
    
    #os.remove(config["playlist_file_path"])
