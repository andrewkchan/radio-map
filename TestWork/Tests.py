import math
pnt_to_song={}
list_of_songs=[[2,3,"song"],[1,1,"a"]]
val=[[1,1],[1,-1],[-1,1],[-1,-1]]
def location_map(list_of_songs):
    for i in val:
        for x in range(2):
            for y in range(2):
                for loc in list_of_songs:
                    temp=[]
                    if math.floor(loc[0])==i[0]*x and math.ceil(loc[1])==i[1]*y:
                        temp.append(loc)
                if not(x==0 or x==90 or y==0 or y==180):
                    pnt_to_song[i[0]*x,i[1]*y]=temp
                elif i==1:
                    pnt_to_song[x,y]=temp

location_map(list_of_songs)
print pnt_to_song