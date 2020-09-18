#!/bin/bash

if [ $1 = "install" ]; then
	cp qyoum.sh /usr/local/bin
	cp youtube-dl-mgr.py /usr/local/bin
	chmod +x /usr/local/bin/qyoum.sh
elif [ $1 = "update" ]; then
    curl -L https://yt-dl.org/downloads/latest/youtube-dl -o /usr/local/bin/youtube-dl
    chmod a+rx /usr/local/bin/youtube-dl
fi
