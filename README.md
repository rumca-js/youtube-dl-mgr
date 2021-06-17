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

Define environment variable YOUTUBE_LIST_FILE, for example in .bashrc.
For example:
```
export YOUTUBE_LIST_FILE=list.txt.
```

# How-To

To add link to download file:
```
python youtube-dl-mgr.py http://youtubelink
```

To download links in download file:
```
python youtube-dl-mgr.py -d
```

The download file can be explicit:
```
python youtube-dl-mgr.py -d -f list.txt
```

To clear the download query file run
```
python youtube-dl-mgr.py -c
```

To play the list. The files are downloaded into working directory and removed after playback.
VLC is used for playback. It needs to be in the PATH.
```
python youtube-dl-mgr.py -p
```

You may want to make an alias for the script. This might be done in .bash_aliases file.
```
alias qy='python3 youtube-dl-mgr.py'
```
After that you can download by simply:
```
qy -d -f list.txt
```
