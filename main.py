import os
import requests

from tqdm import tqdm
from pathlib import Path
from pytube import YouTube
from unidecode import unidecode
from prettytable import PrettyTable

class YoutubeDownloader:
    def __init__(self, youtube_url):
        self.youtube_url = youtube_url
        self.youtube_obj = YouTube(youtube_url)

    def getList(self):
        self.pretty_table = PrettyTable()
        self.pretty_table.field_names = ["No", "Resolution", "FPS", "Filesize", "Type"]

        streams = self.youtube_obj.streams
        for i in range(len(streams)):
            self.pretty_table.add_row([str(i+1), streams[i].resolution, streams[i].fps, self.humanize_filesize(streams[i].filesize), streams[i].mime_type])
        print("Title: " + self.youtube_obj.title)
        print("Author: " + self.youtube_obj.author)
        print("Length: " + self.humanize_time(self.youtube_obj.length))
        print(self.pretty_table)
        return len(streams)

    def download(self, number):
        path = str(os.path.join(Path.home(), "Downloads"))
        if not os.path.exists(path):
            os.mkdir(path)
        url = self.youtube_obj.streams[number].url
        r = requests.get(url, stream=True)
        total_size = self.youtube_obj.streams[number].filesize
        block_size = 1024
        t=tqdm(total=total_size, unit='iB', unit_scale=True)
        file_name = '{}.{}'.format(self.youtube_obj.title, self.youtube_obj.streams[number].subtype)
        # file_name = unidecode(file_name)
        file_name = file_name.replace('/', ' ').replace('\\', ' ').replace('"', ' ').replace(':', ' ').replace('*', ' ').replace('?', ' ').replace('>', ' ').replace('<', ' ').replace('|', ' ')
        file_path = os.path.join(path, file_name)
        with open(file_path, 'wb') as f:
            for data in r.iter_content(block_size):
                t.update(len(data))
                f.write(data)
        t.close()
        print("saved to: " + file_path)

    def humanize_filesize(self, filesize):
        units = ["B", "KB", "MB", "GB"]
        num = 0
        while(filesize / 1024 > 1 and num < len(units)):
            filesize /= 1024
            num += 1
        return "{:.2f} {}".format(filesize, units[num])

    def humanize_time(self, time):
        array = []
        while(time >= 60 and len(array) < 4):
            array.append(time % 60)
            time = int(time/60)
        array.append(time)
        while(len(array) < 4):
            array.append(0)
        return "{:02d}:{:02d}:{:02d}".format(array[2], array[1], array[0])

if __name__ == '__main__':
    os.system('cls' if os.name == 'nt' else 'clear')
    step = 1
    while True:
        if step == 1:
            url = input("youtube url: ")
            youtube = YoutubeDownloader(url)
            os.system('cls' if os.name == 'nt' else 'clear')
            step += 1
        if step == 2:
            total = youtube.getList()
            number = input("Select number to download: ")
            if int(number)-1 >= total or int(number) == 0:
                print("i dont understand")
                input("Press Enter to continue...")
                os.system('cls' if os.name == 'nt' else 'clear')
                continue
            youtube.download(int(number)-1)
            input("Press Enter to continue...")
            os.system('cls' if os.name == 'nt' else 'clear')
            step += 1
        if step == 3:
            print("1. Download another video")
            print("2. Download same video with another format")
            print("3. I want to exit")
            number = input("Is there anything you want to do? ")
            step = int(number)
            if step == 3:
                os.system('cls' if os.name == 'nt' else 'clear')
                break
            elif step > 3:
                print("i dont understand")
                input("Press Enter to continue...")
                os.system('cls' if os.name == 'nt' else 'clear')
                step = 3