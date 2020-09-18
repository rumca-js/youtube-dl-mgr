# Overview

Youtube music download manager. Downloads youtube links as music from the specified input file. The files should be separated by newline.

Comes in a bundle of bash script and python script. The bash script is handy to install & update.

# prerequisites
 - youtube-dl
 - ffmpeg
 - id3v2

# installation
run with root previliges (like with sudo, requires chmod):
```
install.sh install
```

If you do not have youtube-dl installed, then simply run (with root priviliges):
```
install.sh update
```

The command also updates youtube-dl if necessary

Define environment variable YOUTUBE_LIST_FILE, for example in .bashrc.
For example:
```
export YOUTUBE_LIST_FILE=list.txt.
```

# How-To

To add link to download queue. Multiple entries can be added.
```
python youtube-dl-mgr.py http://youtubelink
```

```
python youtube-dl-mgr.py -r
```

To clear the download query file run
```
python youtube-dl-mgr.py -c
```

You may want to make an alias for the script. This might be done in .bash_aliases file.
```
alias qy='python3 youtube-dl-mgr.py'
```
