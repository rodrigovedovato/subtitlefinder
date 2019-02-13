#!/usr/bin/env python3

from xmlrpc.client import ServerProxy
from sys import argv

import os
import utils
import search
import re
import requests

import gzip
import shutil

def get_download_link(file_name):
    os_user = os.environ["OS_USER_NAME"]
    os_password = os.environ["OS_USER_PASSWORD"]
    os_client_user_agent = os.environ["OS_CLIENT_USER_AGENT"]

    with ServerProxy("https://api.opensubtitles.org/xml-rpc") as client:
        login_data = client.LogIn(os_user, os_password, "en", os_client_user_agent)
        user_token = login_data["token"]
        exact_search_results = search.exactSearch(client, file_name, user_token, login_data["data"]["UserPreferedLanguages"])

        if (exact_search_results == "NO_SUBTITLES"):
            return search.textSearch(client, file_name, user_token, login_data["data"]["UserPreferedLanguages"])
        else:
            return exact_search_results

def save_file(download_link, movie_file_name):
    file_data = requests.get(download_link)    
    match_result = re.search('(?<=attachment; filename=\").+(?=\")', file_data.headers["Content-Disposition"])
    file_name = match_result.group(0)    
    target_file_path = os.path.join(os.path.dirname(movie_file_name), file_name)    
    with open(target_file_path, 'wb') as fd:
        for chunk in file_data.iter_content(chunk_size=128):
            fd.write(chunk)
    return target_file_path

def get_subtitle_ext(saved_file):
    # TODO: Improve this
    d = os.path.dirname(saved_file)
    f = os.path.splitext(os.path.basename(saved_file))[0]
    df = os.path.join(d,f)
    return os.path.splitext(os.path.basename(df))[1]

def extract_file(saved_file, movie_file_name):
    subtitle_file_ext = get_subtitle_ext(saved_file)
    subtitle_file_name = os.path.splitext(os.path.basename(movie_file_name))[0]
    target_subtitle_name = subtitle_file_name + subtitle_file_ext
    with gzip.open(saved_file, 'rb') as f_in:
        with open(os.path.join(os.path.dirname(movie_file_name), target_subtitle_name), 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    

file_name = argv[1]

print("Getting subtitle download link...")
download_link = get_download_link(file_name)

if (download_link == "NO_SUBTITLES"):
    print("No subtitles found for this file")
else:
    print("Downloading subtitle...")
    saved_file = save_file(download_link, file_name)
    print("Extracting subtitle...")
    extract_file(saved_file, file_name)
    print("Removing zipped file")
    os.remove(saved_file)
    print("Subtitle successfully downloaded and extracted!")    