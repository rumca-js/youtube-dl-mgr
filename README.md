# youtube-dl-mgr
Youtube download manager. Downloads youtube links as music from the specified input file. The files should be separated by newline.

# prerequisites
 - youtube-dl
 - ffmpeg
 - id3v2
 
# operation
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
