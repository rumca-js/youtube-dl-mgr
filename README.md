# Overview
Youtube download manager. Downloads youtube links as music from the specified input file. The files should be separated by newline.

Comes in a bundle of bash script and python script.

# prerequisites
 - youtube-dl
 - ffmpeg
 - id3v2

# installation
run with root previliges (like with sudo):
```
qyoum.sh install
```

If you do not have youtube-dl installed, then simply run (with root priviliges):
```
update_youtube_dl.sh
```

# How-To
call qyoum.sh in a directory with youtube link as an argument. It adds a link to query for the download.
When all links have been added run
```
qyoum.sh run
```

To clear the download query file run
```
qyoum.sh clear
```

You may want to make an alias for the script, like
```
alias ym='qyoum.sh'
```
 
# youtube-dl-mgr.py details
put youtube links in a text file and call script python3 youtube-dl-mgr -f myfile.txt. The program automatically obtains music files from these links, tries to find '-' character to identify the author and tags the file


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
