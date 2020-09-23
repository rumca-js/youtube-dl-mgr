"""
@artist pzielinski
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

    def download(self, suggested_name=None):
        print("downloading: "+self.link.name)

        proc = subprocess.run(['youtube-dl', '-f','bestaudio[ext=m4a]', self.link.name], stdout=subprocess.PIPE)

        simple_text = proc.stdout.decode("ascii", errors="ignore")

        try:
            out = proc.stdout.decode("utf-8")
            #print(out)
        except Exception as E:
            out = proc.stdout.decode("cp1250")
            #print(out)

        simple_file = self.get_file_name(simple_text)
        real_file = self.get_file_name(out)

        if not os.path.isfile(real_file):
            files = os.listdir()

            simple_files = [ x.encode("ascii",errors="ignore").decode() for x in files]
            for key, item in enumerate(simple_files):
                if item == simple_file:
                    real_file = files[key]

        if suggested_name:
            dst_name = suggested_name
        else:
            dst_name = simple_file

        os.rename( real_file, dst_name)

        return dst_name

    def get_file_name(self, out):
        sp = out.split("\n")
        for line in sp:
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
        print("Converting to mp3...")

        outname = self.name.replace(".m4a", ".mp3")

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

    def __init__(self, file_name, entry=None):
        self.file_name = file_name

        self.song = entry.song
        self.artist = entry.artist
        self.album = entry.album

    def tag(self):
        print("Tagging Song:'{0}' Artist:'{1}' Album:'{2}'".format(self.song, self.artist, self.album))

        subprocess.run(['id3v2', '-t', self.song, '-a', self.artist, '-A', self.album, self.file_name])

    @staticmethod
    def validate():
        try:
            proc = subprocess.run(['id3v2'], stdout=subprocess.PIPE)
        except:
            return False
        return True
    

class Vlc(object):
    def __init__(self, name):
        self.name = name

    def run(self):
        data = subprocess.run(['vlc',self.name, 'vlc://quit'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    @staticmethod
    def validate():
        try:
            proc = subprocess.run(['vlc'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except:
            return False
        return True


class CommandLine(object):

    def __init__(self):
        self.parser = argparse.ArgumentParser(description='Download manager for downloading music from youtube. Please do also buy original copies of the music.')
        self.parser.add_argument('-f', '--filename', dest='filename',
                            help='File name with download list')
        self.parser.add_argument('-d', '--download', action="store_true", dest='download',
                            help='Run conversion using list file')
        self.parser.add_argument('-c', '--clear', action="store_true", dest='clear',
                            help='Clear list file')
        self.parser.add_argument('-a', '--add', dest='add',
                            help='File name to add')
        self.parser.add_argument('-p', '--play', dest='play', action="store_true",
                            help='Plays list')
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


class ConfigurationEntry(object):

    def __init__(self, line):
        self.link = line
        self.artist = ""
        self.album = ""
        self.song = ""

        if line.find(";") >= 0:
            values = line.split(";")
            self.link = values[0]
            if len(values) > 1:
                self.artist = values[1]
            if len(values) > 2:
                self.album = values[2]
            if len(values) > 3:
                self.song = values[3]

    def __str__(self):
        data = "Author:{0}\nAlbum:{1}\nSong:{2}\nLink:{3}".format(self.artist, self.album, self.song, self.link)
        return data

    def get_file_name(self):
        return "{0} - {1} - {2}.m4a".format(self.artist, self.album, self.song)

    def get_dir_name(self):
        return "{0}/{1}".format(self.artist, self.album)


class Configuration(object):

    def __init__(self, file_name):
        with open(file_name) as fh:
            data = fh.read()

        self.entries = []
        
        self.sp = data.split("\n")
        for line in self.sp:
            self.entries.append(ConfigurationEntry(line))

    def get_entries(self):
        return self.entries


class MainProgram(object):

    def __init__(self, cmd):

        if cmd.args.clear:
            os.remove(cmd.args.filename)

        elif cmd.args.add:
            self.add(cmd, cmd.args.add)

        elif cmd.args.link:
            self.add(cmd, cmd.args.link)

        elif cmd.args.download:
            self.download(cmd)

        elif cmd.args.play:
            self.play(cmd)

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

    def download(self, cmd):

        config = Configuration(cmd.args.filename)
        for entry in config.get_entries():

            link = YoutubeLink(entry.link)
            if link.valid:
                print(entry)

                mgr = YoutubeDownloader(link)
                download_name = mgr.download(entry.get_file_name() )

                if download_name:
                    if not FFmpeg.validate():
                        continue

                    ffmpeg = FFmpeg(download_name)
                    mp3_name = ffmpeg.convertToMp3()

                    id3 = Id3(mp3_name, entry)
                    id3.tag()

                    if not os.path.isdir(entry.get_dir_name()):
                        os.makedirs(entry.get_dir_name())

                    dst_name = os.path.join(entry.get_dir_name(), mp3_name)
                    os.rename(mp3_name, dst_name)

    def play(self, cmd):

        config = Configuration(cmd.args.filename)
        for entry in config.get_entries():

            link = YoutubeLink(entry.link)
            if link.valid:
                print( str(entry))

                mgr = YoutubeDownloader(link)
                download_name = mgr.download(entry.get_file_name() )

                if download_name:
                    vlc = Vlc(download_name)
                    vlc.run()

                    os.remove(download_name)
                    print()
    

def main():
    cmd = CommandLine()
    cmd.validate()
    MainProgram(cmd)


if __name__ == "__main__":
    main()
