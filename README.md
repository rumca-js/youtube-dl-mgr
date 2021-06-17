# Overview

Youtube music download manager. Downloads youtube links as music from the specified input file. The files should be separated by newline.

Comes in a bundle of bash script and python script. The bash script is handy to install & update.

# prerequisites

 - youtube-dl (which requires python to be in PATH)
 - ffmpeg
 - id3v2
 - curl for update

# installation

run with root previliges (like with sudo, requires chmod):
```
sudo install.sh install
```

If you do not have youtube-dl installed, then simply run (with root priviliges):
```
sudo install.sh update
```

The command also updates youtube-dl if necessary

# How-To

To create or add link to download file list.txt:
```
python youtube-dl-mgr.py http://youtubelink
```

To download links in download file:
```
python youtube-dl-mgr.py -d
```

To clear the download query file run
```
python youtube-dl-mgr.py -c
```

After adding songs to the download file please edit it to provide Artist, Album and Song names.

To play the list. The files are downloaded into working directory and removed after playback.
VLC is used for playback. It needs to be in the PATH.
```
python youtube-dl-mgr.py -p
```

# Advanced

You do not have to use list.txt file every time. 
Environment variable YOUTUBE_LIST_FILE controls the name of the download queue file.

For example:
```
export YOUTUBE_LIST_FILE=list.txt.
```

The download file can also be explicit:
```
python youtube-dl-mgr.py -d -f list.txt
```

You may want to make an alias for the script. This might be done in .bash_aliases file.
```
alias qy='python3 youtube-dl-mgr.py'
```

After that you can download by simply:
```
qy -d -f list.txt
```

