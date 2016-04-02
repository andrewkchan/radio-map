import html_parser

songList = html_parser.read('first20')
for song in songList:
    print('Song:', song.songName)
    print('SongID:', song.songLink)
    print('Artist:', song.artistName)
    print('ArtistID:', song.artistLink)
    print('Date:', song.date)
    print('')

import urllib.request

#for song in songList:
