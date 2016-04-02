import math
pnt_to_song={}
"""list of songs is place holder"""
list_of_songs=[["x","y","song"],[]]
val=[[1,1],[1,-1],[-1,1],[-1,-1]]
def location_map(list_of_songs):
    for i in val:
        for x in range(91):
            for y in range(181):
                for loc in list_of_songs:
                    temp=[]
                    if math.floor(loc[0])==i[0]*x and math.ceil(loc[1])==i[1]*y:
                        temp.append(loc)
                if not(x==0 or x==90 or y==0 or y==180):
                    pnt_to_song[i[0]*x,i[1]*y]=temp
                elif i==1:
                    pnt_to_song[x,y]=temp

"""car loc is place holder"""
car_loc=["x","y"]
def nearest(car_loc):
    x=math.floor(car_loc[0])
    y=math.ceil(car_loc[1])
    search_block=[[0,0]]
    while check_empty(x,y,search_block)==False:
        search_block=block_make(max(search_block)[0]+2)
    possible=[]
    for sub in search_block:
        x,y=prune_ends(x+sub[0],y+sub[1])
        for song in pnt_to_song[x,y]:
            distance=math.sqrt(car_loc[0]-song[0],car_loc[1]-song[1])
            if possible==[] or distance<=possible[0]:
                possible=[distance,song]
    return possible[1]

def prune_ends(x,y):
    if x>90:
        x=-180+x
    elif x<=-90:
        x=180+x
    if y>180:
        y=-360+y
    elif y<=-180:
        y=360+y
    return x,y

def check_empty(x,y,search):
    for sub in search:
        if pnt_to_song[x+sub[0],y+sub[1]]!=[]:
            return True
    return False
    
            
def block_make(span):
    search_block=[]
    for i in range(span):
        for j in range(span):
            search_block.append([i,j])
            if i!=0 or j!=0:
                search_block.append([-i,-j])
    return search_block
        