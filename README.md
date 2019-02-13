# opensubtitles.org subtitle finder

This is a Python script that automates subtitle downloading using opensubtitles.org database.

## Setup

Due to API restrictions, you must create a valid opensubtitles.org user agent (https://bit.ly/2SJi7Of) and register an user at opensubtitles.org. After doing that, configure the following OS environment variables:

**For testing / development purposes, *TemporaryUserAgent* can be used**

* OS_USER_NAME: Your opensubtitles.org user name
* OS_USER_PASSWORD: Your opensubtitles.org password
* OS_CLIENT_USER_AGENT: The user agent you registered

## Running

Running this script is simple. Just execute `subtitlefinder.py <your_file_path>` using your shell. The script automatically searches, downloads and extracts the subtitle file

## How it works

This script uses the OS HASH algorithm (https://bit.ly/2Svb1h2) to generate a hash for your video file. If it doesn't find any matching subtitles, it uses the full text search provided by the opensubtitles API. 

In the case a full text search is necessary, we rank the subtitles using three properties (in this order of priority): SubRating, SubDownloadCount and UserRank.
