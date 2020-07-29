# Overview
Youtube download manager. Downloads youtube links as music from the specified input file. The files should be separated by newline.

Comes in a bundle of bash script and python script.

# prerequisites
 - youtube-dl
 - ffmpeg
 - id3v2

# installation
run with root previliges (like with sudo, requires chmod):
```
qyoum.sh install
```

Define environment variable YOUTUBE_LIST_FILE, for example in .bashrc.
For example:
```
export YOUTUBE_LIST_FILE=list.txt.

If you do not have youtube-dl installed, then simply run (with root priviliges):
```
update_youtube_dl.sh
```

# How-To
call qyoum.sh with link as an argument to queue the file for download.
```
qyoum.sh http://youtubelink
```
call qyoum.sh run to download.
```
qyoum.sh run
```

To clear the download query file run
```
qyoum.sh clear
```

You may want to make an alias for the script. This might be done in .bash_aliases file.
```
alias qy='qyoum.sh'
```
 
# youtube-dl-mgr.py details
These details are not necessary for the user experience. The script puts youtube links in a text file and call script python3 youtube-dl-mgr -f myfile.txt. The program automatically obtains music files from these links, tries to find '-' character to identify the author and tags the file


```
usage: youtube-dl-mgr.py [-h] [-f FILENAME] [-o OUTPUT]

Download manager for downloading music from youtube. Please do also buy original copies of the music.

optional arguments:
  -h, --help            show this help message and exit
  -f FILENAME, --filename FILENAME
                        File name with download list
  -o OUTPUT, --output OUTPUT
                        Output directory
```
