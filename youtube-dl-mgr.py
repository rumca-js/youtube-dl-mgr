"""
@author pzielinski
@description:

prerequisites:
 - ffmpeg
 - youtube-dl
 - id3v2
 
"""
import argparse
import os
import sys
import subprocess
import pathlib


YOUTUBE_VARIABLE_NAME = "YOUTUBE_LIST_FILE"


class YoutubeLink(object):
    def __init__(self, wholename):
        if wholename.strip() == "":
            self.valid = False
        else:
            self.valid = True

        self.wholename = wholename
        self.name = wholename
        
        wh1 = self.wholename.find("&")
        if wh1 > 0:
            self.name = self.wholename[:wh1]


class YoutubeDownloader(object):
    def __init__(self, link):
        self.link = link

    def download(self):
        print("downloading: "+self.link.name)
        proc = subprocess.run(['youtube-dl', '-f','bestaudio[ext=m4a]', self.link.name], stdout=subprocess.PIPE)
        out = proc.stdout.decode("utf-8")
        print(out)
        sp = out.split("\n")
        for line in sp:
            print(line)
            wh1 = line.find("Destination")
            if wh1 > 0:
                return line[wh1+13:]

    @staticmethod
    def validate():
        try:
            proc = subprocess.run(['youtube-dl'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except:
            return False
        return True


class FFmpeg(object):
    def __init__(self, name):
        self.name = name

    def convertToMp3(self):
        outname = self.name.replace(".m4a", ".mp3")
        wh1 = outname.rfind('-')
        if wh1 > 0:
            outname=outname[:wh1]+".mp3"

        data = subprocess.run(['ffmpeg', '-y', '-i', self.name, '-vn', outname], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        os.remove(self.name)

        return outname

    @staticmethod
    def validate():
        try:
            proc = subprocess.run(['ffmpeg'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except:
            return False
        return True


def string_find_first_of(akey):
    if akey == -1:
        return 1000
    else:
        return akey


class Id3(object):
    def __init__(self, name):
        self.fullname = name
        self.name = name[:-4]

        self.song = self.name
        self.artist = self.name

        wh1 = self.name.find("-")
        wh2 = self.name.find("–")
        wh3 = self.name.find(':')

        table = [wh1, wh2, wh3]
        value = min(table, key=string_find_first_of)

        if value != -1:
            self.artist = self.name[:value-1]
            self.song = self.name[value + 2 :]

    def tag(self):
        self.album = self.artist
        print("Tagging Song:'{0}' Artist:'{1}' Album:'{2}'".format(self.song, self.artist, self.album))
        subprocess.run(['id3v2', '-t', self.song, '-a', self.artist, '-A', self.album, self.fullname])

    @staticmethod
    def validate():
        try:
            proc = subprocess.run(['id3v2'], stdout=subprocess.PIPE)
        except:
            return False
        return True


class CommandLine(object):

    def __init__(self):
        self.parser = argparse.ArgumentParser(description='Download manager for downloading music from youtube. Please do also buy original copies of the music.')
        self.parser.add_argument('-f', '--filename', dest='filename',
                            help='File name with download list')
        self.parser.add_argument('-r', '--run', action="store_true", dest='run',
                            help='Run conversion using list file')
        self.parser.add_argument('-c', '--clear', action="store_true", dest='clear',
                            help='Clear list file')
        self.parser.add_argument('-a', '--add', dest='add',
                            help='File name to add')
        self.parser.add_argument('-o', '--output', dest='output', default='.',
                            help='Output directory')
        self.parser.add_argument('link', nargs='?', default="", help='YouTube link to add')

        self.args = self.parser.parse_args()

    def validate(self):

        if self.args.filename is None:
            if YOUTUBE_VARIABLE_NAME not in os.environ:
                print("Either -f option has to be specified or '{0}' environment variable has to be set".format(YOUTUBE_VARIABLE_NAME))
                sys.exit(1)
            else:
                self.args.filename = os.environ[YOUTUBE_VARIABLE_NAME]

        if self.args.add is not None:
            return
        if self.args.clear is not None:
            return
        if self.args.link is not None:
            return

        if not os.path.isfile(self.args.filename):
            print("File name does not exist '{0}'".format(self.args.filename))
            sys.exit(1)

        if not os.path.isfile(self.args.filename):
            print("File name does not exist {0}".format(self.args.filename))
            sys.exit(1)

        if not os.path.isdir(self.args.output):
            print("Dir name does not exist {0}".format(self.args.output))
            sys.exit(1)

        if not YoutubeDownloader.validate():
            print("youtubut-dl is not present in your system");
            sys.exit(2)

        if not FFmpeg.validate():
            print("ffmpeg is not present in your system");
            sys.exit(2)

        if not Id3.validate():
            print("id3v2 is not present in your system");
            sys.exit(2)


class MainProgram(object):

    def __init__(self, cmd):

        if cmd.args.clear:
            os.remove(cmd.args.filename)

        elif cmd.args.add:
            self.add(cmd, cmd.args.add)

        elif cmd.args.link:
            self.add(cmd, cmd.args.link)

        elif cmd.args.run:
            self.process(cmd)

    def add(self, cmd, text):
        data = ""

        if os.path.isfile(cmd.args.filename):
            with open(cmd.args.filename, 'r') as fh:
                data = fh.read()

        if data == "":
            toadd = text
        else:
            toadd = data + "\n" + text

        with open(cmd.args.filename, 'w') as fh:
            fh.write(toadd)

    def process(self, cmd):
        with open(cmd.args.filename) as fh:
            data = fh.read()
        
        sp = data.split("\n")
        for line in sp:
            link = YoutubeLink(line)
            if link.valid:
                mgr = YoutubeDownloader(link)
                fname = mgr.download()
                if fname:
                    ffmpeg = FFmpeg(fname)
                    out = ffmpeg.convertToMp3()

                    id3 = Id3(out)
                    id3.tag()
    

def main():
    cmd = CommandLine()
    cmd.validate()
    MainProgram(cmd)


if __name__ == "__main__":
    main()
