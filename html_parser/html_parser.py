# Brian Levis
# 4/1/16

import urllib.request, wikipedia

class Song:
    def __init__(self):
        self.date = ''
        self.songName = ''
        self.songLink = ''
        self.artistName = ''
        self.artistLink = ''
        self.artistHometown = ''

def read(file_name):
    file = open(file_name + '.htm', 'r')
    n = -1
    stringList = []
    for line in file:
        if line[:4] == ' <tr':
            n += 1
            stringList += ['']
        if n != -1 and line[:5] != ' </tr':
            stringList[n] += line
    song_list = []
    for string in stringList:
        tagNum = -1
        song = Song()
        for i in range(len(string)):
            if string[i:i+3] == '<td':
                tagNum += 1
            if tagNum == 1:
                if string[i] == '>':
                    while string[i + 1] != '<':
                        i += 1
                        song.date += string[i]
            elif tagNum == 2:
                if string[i - 6:i] == '/wiki/':
                    while string[i] != '"':
                        song.artistLink += string[i]
                        i += 1
                elif string[i - 7:i] == 'title="':
                    while string[i] != '"':
                        song.artistName += string[i]
                        i += 1
            elif tagNum == 3:
                if string[i - 6:i] == '/wiki/':
                    while string[i] != '"':
                        song.songLink += string[i]
                        i += 1
                elif string[i - 7:i] == 'title="':
                    while string[i] != '"':
                        song.songName += string[i]
                        i += 1
        song_list += [song]
    for song in song_list:
        artist_hometown(song)
    return song_list

def artist_hometown(song):
        artist_page = urllib.request.urlopen("https://en.wikipedia.org/w/index.php?action=raw&title=" + song.artistLink).read()
        print('fetched page for', song.songName)
        hometown = ''
        for i in range(len(artist_page)):
            if artist_page[i - 11:i] == 'birth_place':
                print('asdf')
                while artist_page[i - 2:i] != '[[':
                    i += 1
                while artist_page[i] != ']':
                    hometown += artist_page[i]
                    i += 1
                print(hometown)
        #hometown_page = urllib.request.urlopen("https://en.wikipedia.org/w/index.php?action=raw&title=" + hometown).read()
