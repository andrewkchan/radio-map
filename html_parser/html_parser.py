import urllib.request, wikipedia, sys

class Song:
    def __init__(self):
        self.date = ''
        self.songName = ''
        self.songLink = ''
        self.artistName = ''
        self.artistLink = ''
        self.lat = ''
        self.long = ''

def read(file_name):
    print('Reading...', end='')
    file = open(file_name + '.htm', 'r')
    print('Done!')
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
    x = 1
    for song in song_list:
        try:
            artist_hometown(song)
        except:
            print('Failed on ' + song.songName + '!')
        if x % 10 == 0:
            print(str(10 * x // 105) + '%')
        x += 1
    return song_list

def artist_hometown(song):
        #if int(song.date[len(song.date)-2:]) != year % 100:
        #    year += 1
        #    print('Determining artists and hometowns for ' + year + '!')
        artist_page = urllib.request.urlopen("https://en.wikipedia.org/w/index.php?action=raw&title=" + song.artistLink).read()
        hometown = ''
        for j in range(len(artist_page)):
            if artist_page[j - 11:j] == b'birth_place':
                while artist_page[j - 2:j] != b'[[':
                    j += 1
                while artist_page[j:j+ 1] != b']' and artist_page[j:j + 1] != b'|':
                    hometown += artist_page[j:j + 1].decode('ascii')
                    j += 1
                hometown = title_to_id(hometown)
                #print("Hometown: " + hometown)
                hometown_page = urllib.request.urlopen("https://en.wikipedia.org/w/index.php?action=raw&title=" + hometown).read()
                latd = latm = lats = latNS = ''
                longd = longm = longs = longEW = ''
                for i in range(len(hometown_page) - 100):
                    if False and i > 9 and i < 1000 and hometown_page[i - 8:i] == b'{{Coord|':
                        while hometown_page[i:i + 1] != b'|':
                            latd = hometown_page[i:i + 1].decode('ascii')
                            i += 1
                        i += 1
                        while hometown_page[i:i + 1] != b'|':
                            latm = hometown_page[i:i + 1].decode('ascii')
                            i += 1
                        i += 1
                        while hometown_page[i:i + 1] != b'|':
                            lats = hometown_page[i:i + 1].decode('ascii')
                            i += 1
                        i += 1
                        while hometown_page[i:i + 1] != b'|':
                            latNS = hometown_page[i:i + 1].decode('ascii')
                            i += 1
                        i += 1
                        while hometown_page[i:i + 1] != b'|':
                            longd = hometown_page[i:i + 1].decode('ascii')
                            i += 1
                        i += 1
                        while hometown_page[i:i + 1] != b'|':
                            longm = hometown_page[i:i + 1].decode('ascii')
                            i += 1
                        i += 1
                        while hometown_page[i:i + 1] != b'|':
                            longs = hometown_page[i:i + 1].decode('ascii')
                            i += 1
                        i += 1
                        while hometown_page[i:i + 1] != b'|':
                            longEW = hometown_page[i:i + 1].decode('ascii')
                            i += 1
                    check = False
                    for k in range(5):
                        if hometown_page[i - 9 + k:i - 8 + k] == b'|':
                            check = True
                    if check:
                        if hometown_page[i - 4:i] == b'latd' or hometown_page[i - 5:i] == b'lat_d':
                            while hometown_page[i:i + 1] == b'=' or hometown_page[i:i + 1] == b' ':
                                i += 1
                            while hometown_page[i:i + 1] != b'\n' and hometown_page[i:i + 1] != b' ' and hometown_page[i:i + 1] != b'|':
                                latd += hometown_page[i:i + 1].decode('ascii')
                                i += 1
                        if hometown_page[i - 4:i] == b'latm' or hometown_page[i - 5:i] == b'lat_m':
                            while hometown_page[i:i + 1] == b'=' or hometown_page[i:i + 1] == b' ':
                                i += 1
                            while hometown_page[i:i + 1] != b'\n' and hometown_page[i:i + 1] != b' ' and hometown_page[i:i + 1] != b'|':
                                latm += hometown_page[i:i + 1].decode('ascii')
                                i += 1
                        if hometown_page[i - 4:i] == b'lats' or hometown_page[i - 5:i] == b'lat_s':
                            while hometown_page[i:i + 1] == b'=' or hometown_page[i:i + 1] == b' ':
                                i += 1
                            while hometown_page[i:i + 1] != b'\n' and hometown_page[i:i + 1] != b' ' and hometown_page[i:i + 1] != b'|':
                                lats += hometown_page[i:i + 1].decode('ascii')
                                i += 1
                        if hometown_page[i - 5:i] == b'latNS' or hometown_page[i - 6:i] == b'lat_NS':
                            while hometown_page[i:i + 1] == b'=' or hometown_page[i:i + 1] == b' ':
                                i += 1
                            while hometown_page[i:i + 1] != b'\n' and hometown_page[i:i + 1] != b' ' and hometown_page[i:i + 1] != b'|':
                                latNS += hometown_page[i:i + 1].decode('ascii')
                                i += 1
                        if hometown_page[i - 5:i] == b'longd' or hometown_page[i - 6:i] == b'long_d':
                            while hometown_page[i:i + 1] == b'=' or hometown_page[i:i + 1] == b' ':
                                i += 1
                            while hometown_page[i:i + 1] != b'\n' and hometown_page[i:i + 1] != b' ' and hometown_page[i:i + 1] != b'|':
                                longd += hometown_page[i:i + 1].decode('ascii')
                                i += 1
                        if hometown_page[i - 5:i] == b'longm' or hometown_page[i - 6:i] == b'long_m':
                            while hometown_page[i:i + 1] == b'=' or hometown_page[i:i + 1] == b' ':
                                i += 1
                            while hometown_page[i:i + 1] != b'\n' and hometown_page[i:i + 1] != b' ' and hometown_page[i:i + 1] != b'|':
                                longm += hometown_page[i:i + 1].decode('ascii')
                                i += 1
                        if hometown_page[i - 5:i] == b'longs' or hometown_page[i - 6:i] == b'long_s':
                            while hometown_page[i:i + 1] == b'=' or hometown_page[i:i + 1] == b' ':
                                i += 1
                            while hometown_page[i:i + 1] != b'\n' and hometown_page[i:i + 1] != b' ' and hometown_page[i:i + 1] != b'|':
                                longs += hometown_page[i:i + 1].decode('ascii')
                                i += 1
                        if hometown_page[i - 6:i] == b'longEW' or hometown_page[i - 7:i] == b'long_EW':
                            while hometown_page[i:i + 1] == b'=' or hometown_page[i:i + 1] == b' ':
                                i += 1
                            while hometown_page[i:i + 1] != b'\n' and hometown_page[i:i + 1] != b' ' and hometown_page[i:i + 1] != b'|':
                                longEW += hometown_page[i:i + 1].decode('ascii')
                                i += 1
                #print(latd + 'd' + latm + 'm' + lats + 's' + latNS)
                #print(longd + 'd' + longm + 'm' + longs + 's' + longEW)
                if latNS == 'S':
                    latNS = -1
                else:
                    latNS = 1
                if longEW == 'W':
                    longEW = -1
                else:
                    longEW = 1
                if latd == '':
                    latd = '0'
                if latm == '':
                    latm = '0'
                if lats == '':
                    lats = '0'
                if longd == '':
                    longd = '0'
                if longm == '':
                    longm = '0'
                if longs == '':
                    longs = '0'
                try:
                    song.lat = (float(latd) + float(latm) / 60 + float(lats) / 60 / 60) * latNS
                    song.long = (float(longd) + float(longm) / 60 + float(longs) / 60 / 60) * longEW
                except:
                    print('Failed on ' + song.songName + '!')
                    print(str(latd) + 'd' + str(latm) + 'm' + str(lats) + 's' + str(latNS))
                    print(str(longd) + 'd' + str(longm) + 'm' + str(longs) + 's' + str(longEW))
                break

def title_to_id(title):
    id = ''
    for c in title:
        if c == ' ':
            id += '_'
        else:
            id += c
    return id
