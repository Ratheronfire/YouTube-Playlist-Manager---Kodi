from __future__ import division

__author__ = "David"

import json
import xbmc
import xbmcgui
from find_account_playlists import find_account_playlists
from resources.config import config

def update_existing_uploaders():
    with open(config["video_prefs_path"], "r") as prefs:
        prefs_json = json.load(prefs)
    
    uploader_count = len(prefs_json["uploaders"])
    uploaders_processed = 0
    
    progress_bar = xbmcgui.DialogProgress()
    progress_bar.create("Searching for New Videos", "0 uploaders processed.")

    for uploader in prefs_json["uploaders"]:
        if progress_bar.iscanceled():
            return

        find_account_playlists(uploader, False)

        uploaders_processed += 1
        progress_bar.update(int(100 * uploaders_processed / uploader_count), str(uploaders_processed) + " uploaders processed.")
