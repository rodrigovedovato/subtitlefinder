# opensubtitles.org subtitle finder

This is a Python script that automates subtitle downloading using opensubtitles.org database.

## Setup

As of now, you must create a valid opensubtitles.org user agent (https://bit.ly/2SJi7Of) and register an user at opensubtitles.org. After doing that, configure the following OS environment variables:

**For testing / development purposes, *TemporaryUserAgent* can be used**

* OS_USER_NAME: Your opensubtitles.org user name
* OS_USER_PASSWORD: Your opensubtitles.org password
* OS_CLIENT_USER_AGENT: The user agent you registered

## Running

Running this script is simple. Just execute `subtitlefinder.py <your_file_path>` using your shell. The script automatically searches, downloads and extracts the subtitle file
