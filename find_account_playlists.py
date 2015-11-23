__author__ = "David"

import json
import sys
import xbmc
import xbmcgui
from codecs import open
from add_playlist import add_playlist
from youtube_playlist import send_get_request
from resources.config import config

uploader_id = str()

def usage_message():
    print("USAGE: {0} [id/username] uploader-details".format(sys.argv[0]))
    exit(-1)

def process_pages(json_page):
    playlists = dict()

    finished = False

    while not finished:
        if "items" not in json_page:
            continue

        playlist_entries = json_page["items"]

        for playlist in playlist_entries:
            playlists[playlist["snippet"]["title"]] = playlist["id"]

        if "nextPageToken" in json_page:
            json_page = send_get_request("https://www.googleapis.com/youtube/v3/playlists?part=snippet&channelId={0}&"
                                     "pageToken={1}&fields=items(id%2Csnippet)%2CnextPageToken%2CprevPageToken&"
                                     "key={2}".format(uploader_id, json_page["nextPageToken"], config["api_key"]))
        else:
            finished = True

    return playlists


def process_playlists(playlists):
    playlists_to_add = list()
    adding_all = False

    with open(config["playlist_prefs_path"], "r") as data:
        playlist_json = json.load(data)

    for (playlist_title, playlist_id) in playlists.items():
        decided = False

        while not decided and not adding_all:

            try:
                should_add_bool = playlist_json[playlist_id]

                if should_add_bool:
                    should_add = 0
                else:
                    should_add = 1
            except KeyError:  # no preference for this playlist was found
                should_add_dialog = xbmcgui.Dialog()
                should_add = should_add_dialog.select("Do you want to add " + playlist_title + " to the collection?", ["Yes", "No", "Add All"])

            if should_add == 0:
                print("Okay, I'll add %s." % playlist_title)
                playlist_json[playlist_id] = True
                playlists_to_add.append(playlist_id)
                decided = True
            elif should_add == 1:
                playlist_json[playlist_id] = False
                decided = True
            elif should_add == 2:
                adding_all = True
                playlists_to_add = playlists.values()
                break

    for playlist in playlists_to_add:
        add_playlist(playlist)

    with open(config["playlist_prefs_path"], "w") as playlist_prefs:
        json.dump(playlist_json, playlist_prefs, indent=2)


def find_account_playlists(input_var, input_is_username):
    global uploader_id

    if input_is_username:
        id_response_json = send_get_request("https://www.googleapis.com/youtube/v3/channels?part=snippet"
                                        "&forUsername={0}&fields=items%2Fid&key={1}".format(input_var,
                                                                                            config["api_key"]))

        if len(id_response_json["items"]) == 0:
            print("Error finding playlists for", input_var)
            return(-1)

        uploader_id = id_response_json["items"][0]["id"]
    else:
        uploader_id = input_var

    playlists_response_json = send_get_request("https://www.googleapis.com/youtube/v3/playlists?part=snippet&"
                                               "channelId={0}&fields=items(id%2Csnippet)%2CnextPageToken%2C"
                                               "prevPageToken&key={1}".format(uploader_id, config["api_key"]))

    playlists = process_pages(playlists_response_json)

    process_playlists(playlists)
