#!/usr/bin/env python3

from xmlrpc.client import ServerProxy
from sys import argv

import os
import utils
import search

file_name = argv[1]

os_user = os.environ["OS_USER_NAME"]
os_password = os.environ["OS_USER_PASSWORD"]
os_client_user_agent = os.environ["OS_CLIENT_USER_AGENT"]

with ServerProxy("https://api.opensubtitles.org/xml-rpc") as client:
    login_data = client.LogIn(os_user, os_password, "en", os_client_user_agent)
    user_token = login_data["token"]
    search_result = search.textSearch(client, file_name, user_token, login_data["data"]["UserPreferedLanguages"])

    print(search_result)
