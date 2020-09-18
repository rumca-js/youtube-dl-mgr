#!/bin/bash

if [ $1 = "install" ]; then
	cp youtube-dl-mgr.py /usr/local/bin
elif [ $1 = "update" ]; then
    curl -L https://yt-dl.org/downloads/latest/youtube-dl -o /usr/local/bin/youtube-dl
    chmod a+rx /usr/local/bin/youtube-dl
fi
