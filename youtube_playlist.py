__author__ = "David"

# from play_videos import play_videos
# from add_playlist import add_playlist
# from find_account_playlists import find_account_playlists
# from generate_playlist import generate_playlist
# from update_existing_uploaders import update_existing_uploaders

# from oauth2client.client import flow_from_clientsecrets
# from oauth2client.client import OAuth2WebServerFlow
import lib.requests
import json
import os

default_config = {'players': [], 'video_prefs_path': os.getcwd() + "/video_prefs.json",
                  'playlist_prefs_path': os.getcwd() + "\\playlist_prefs.json",
                  'playlist_file_path': os.getcwd() + "\\videos.pls", 'api_key': ""}

def prompt_for_api_key():
    print("No valid API key was found.  You must generate one through https://console.developers.google.com/"
          ", and put the API key in configs.json.")
    # TODO: implement better method for generating API key

    exit(1)

def send_get_request(url):
    response_json = dict()

    try:
        response_json = lib.requests.get(url).json()
    except Exception as e:
        print("Error trying to send GET request for {0}\n Error {1} - {2}".format(url, type(e), e.args))

    if "error" in response_json:
        if response_json["error"]["errors"][0]["reason"] == "keyInvalid":
            prompt_for_api_key()

    return response_json
