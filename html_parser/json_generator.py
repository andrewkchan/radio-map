import html_parser, json, youtube_search

song_list = html_parser.read('first20')

file = open('dicdump.json', 'w')

print('Querying YouTube...', end='')
x = 0
largeArray = []
for song in song_list:
    if song.lat != '' and song.long != '' and song.songName != '' and song.artistName != '':
        x += 1
        dict = {}
        dict['lat'] = song.lat
        dict['lng'] = song.long
        dict['songName'] = song.songName
        dict['artistName'] = song.artistName
        dict['youtubeLink'] = youtube_search.video(song.songName)
        largeArray += [dict]
        print(str(x / 600) + '%')
buckets = {}
for song in largeArray:
    key = str(round(song['lat']))+","+str(round(song['lng']))
    if not key in buckets:
        buckets[key] = []
    buckets[key] += song
json.dump(buckets, file)
print('Done!')
print(str(x / len(song_list)) + '% translated.')
