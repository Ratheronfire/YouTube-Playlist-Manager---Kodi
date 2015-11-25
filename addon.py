import sys
import urllib
import urlparse
import xbmcaddon
import xbmcplugin
import xbmcgui
import xbmc
import os
from play_videos import *
from update_existing_uploaders import *
from find_account_playlists import *
 
addon = xbmcaddon.Addon()
addonname = addon.getAddonInfo('name')

base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
args = urlparse.parse_qs(sys.argv[2][1:])

def make_url(params):
    return base_url + "?" + urllib.urlencode(params)

mode = args.get("mode", None)

if mode is None:
    play_url = make_url({"mode":"play"})
    play_entry = xbmcgui.ListItem("Play Videos", iconImage="DefaultFolder.png")
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=play_url, listitem=play_entry, isFolder=True)
    
    edit_url = make_url({"mode":"edit"})
    edit_entry = xbmcgui.ListItem("Edit Playlists", iconImage="DefaultFolder.png")
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=edit_url, listitem=edit_entry, isFolder=True)
    
    add_url = make_url({"mode":"add"})
    add_entry = xbmcgui.ListItem("Add Playlists", iconImage="DefaultFolder.png")
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=add_url, listitem=add_entry, isFolder=True)

    update_url = make_url({"mode":"update"})
    update_entry = xbmcgui.ListItem("Update Collection", iconImage="DefaultFolder.png")
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=update_url, listitem=update_entry, isFolder=True)
    
    xbmcplugin.endOfDirectory(addon_handle)
elif mode[0] == "play":
    play_videos()
elif mode[0] == "edit":
    with open(config["video_prefs_path"], encoding="utf-8") as videos_file:
        videos_json = json.load(videos_file)
    
    for uploader in videos_json["uploaders"]:
        uploader_url = make_url({"mode":"edit_uploader","uploader":uploader})
        uploader_entry = xbmcgui.ListItem(videos_json["uploaders"][uploader]["name"], iconImage="DefaultFolder.png")
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=uploader_url, listitem=uploader_entry, isFolder=True)
    
    xbmcplugin.endOfDirectory(addon_handle)
elif mode[0] == "edit_uploader":
    uploader_id = args.get("uploader", None)[0]

    playlists = get_account_playlists(uploader_id, False)

    for (playlist_title, playlist_id) in playlists.items():
        playlist_url = make_url({"mode":"edit_playlist","playlist":playlist_id})
        playlist_entry = xbmcgui.ListItem(playlist_title, iconImage="DefaultFolder.png")
        xbmcplugin.addDirectoryItem(handle=addon_handle, url=playlist_url, listitem=playlist_entry, isFolder=True)

    xbmcplugin.endOfDirectory(addon_handle)
elif mode[0] == "edit_playlist":
    playlist_id = args.get("playlist", None)[0]

    if not os.access(config["playlist_prefs_path"], os.F_OK):
        with open(config["playlist_prefs_path"], "w") as data:
            data.write("{}")

    with open(config["playlist_prefs_path"], "r") as data:
        playlist_json = json.load(data)

    dialog_string = "Do you want to include this playlist?  It is currently not included."
    if playlist_id in playlist_json and playlist_json[playlist_id]:
        dialog_string = "Do you want to include this playlist?  It is currently included."

    playlist_dialog = xbmcgui.Dialog()

    include_decision = playlist_dialog.select(dialog_string, ["Yes", "No", "Remove Preference", "Cancel"])

    if include_decision == 3:
        exit(0)
    elif include_decision == 0:
        playlist_json[playlist_id] = True
    elif include_decision == 1:
        playlist_json[playlist_id] = False
    elif include_decision == 2:
        del playlist_json[playlist_id]

    with open(config["playlist_prefs_path"], "w") as playlist_prefs:
        json.dump(playlist_json, playlist_prefs, indent=2)

elif mode[0] == "update":
    update_existing_uploaders()
