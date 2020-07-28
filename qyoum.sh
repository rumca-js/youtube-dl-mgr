#!/bin/bash

# Run this script with install parameter to install it.
# Then run this script with a link you wish to download. You can query multiple files like that.
# When you are raedy run this script with run parameter.

if [ $1 = "install" ]; then
	cp qyoum.sh /usr/local/bin
	cp youtube-dl-mgr.py /usr/local/bin
	chmod +x /usr/local/bin/qyoum.sh
elif [ $1 = "run" ]; then
	[[ -n $YOUTUBE_LIST_FILE ]] && python3 /usr/local/bin/youtube-dl-mgr.py -f $YOUTUBE_LIST_FILE
elif [ $1 = "clear" ]; then
	[[ -n $YOUTUBE_LIST_FILE ]] && truncate -s 0 $YOUTUBE_LIST_FILE
else
	[[ -n $YOUTUBE_LIST_FILE ]] && echo "$1" >> $YOUTUBE_LIST_FILE
fi
