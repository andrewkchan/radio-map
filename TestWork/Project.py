import sys
import random
from __builtin__ import int
sys.setrecursionlimit(100000)
class Field_Test(object):
    '''field: holds values associated with the field
    ops: holds values to check spacing, piece, and opposite side to a selected direction
    bool: useful global bool variable
    memoryBank: holds the values of the current path. each entry includes row, column, side, and total length of the path
    obstacle: records each unsuccessful turn that resulted in early termination of memoryBank. each entry includes row, column, side, and total length of the path
    temporaryBank: holds the longest memoryBank path for a specific wall iteration
    retry: if true, restarts that wall creating process at a different column or row level. if false, then path successfully completed its full length
    side_count: total number of times a specific side has tried to create a wall''' 
    field=[]
    ops={"left":[[1,-1],[0,-1],[-1,-1],[0,-2],[1,-2],[-1,-2],["-"],["right"]],"right":[[1,1],[0,1],[-1,1],[0,2],[1,2],[-1,2],["-"],["left"]],
         "up":[[-1,1],[-1,0],[-1,-1],[-2,0],[-2,1],[-2,-1],["|"],["down"]],"down":[[1,1],[1,0],[1,-1],[2,0],[2,1],[2,-1],["|"],["up"]]}
    bool=True
    memoryBank=[]
    obstacle=[]
    temporaryBank=[]
    retry=False
    side_count=0
    row_col_fix=[]
    
    
    def __init__(self):
        self.row_input=int(raw_input("Number of rows?"))
        self.col_input=int(raw_input("Number of columns?"))
        self.number_of_walls=int(raw_input("Number of walls?"))
        self.wall_length=int(raw_input("Length of walls?"))
        self.wall_cycle=[[0,0,1,"up"],[self.row_input-1,0,2,"left"],[self.row_input-1,self.col_input-1,1,"down"],[0,self.col_input-1,2,"right"]]
        
    
    '''creates the field'''
    def field_create(self):
        for _ in range(self.row_input):
            row=[]
            for _ in range(self.col_input):
                row.append(" ")
            self.field.append(row)
        return self.field
    
    '''clears the field'''
    def field_clear(self):
        for i in range(self.row_input):
            for j in range(self.col_input):
                self.field[i][j]=" "
                
    '''displays the field'''
    def display_field(self):
        print " -"*self.col_input
        for i in range(self.row_input):
            print "|",
            sys.stdout.write("%s" % self.field[i][0])
            for j in range(1,self.col_input):
                sys.stdout.write("%2s" % self.field[i][j])
            sys.stdout.write("|") 
            print
        print " -"*self.col_input
        
    '''run field to check for bugs'''
    def field_run(self):
        for _ in range(100):
            self.field_create()
            self.set_walls()
            self.display_field()
            self.field_clear()
            print "next"
    
    '''set orientation of wall'''        
    def set_walls(self):
        for i in range(self.number_of_walls):
            try:
                self.wall_create(self.wall_cycle[i][0], self.wall_cycle[i][1], self.wall_cycle[i][2], self.wall_cycle[i][3])
            except IndexError:
                i=i%4
                self.wall_create(self.wall_cycle[i][0], self.wall_cycle[i][1], self.wall_cycle[i][2], self.wall_cycle[i][3])
                
    '''deals with creation of the wall,
    resets values, sets down the first piece
    where the code will start and end for the creation process'''
    def wall_create(self,row,column,fix,side):
        self.memoryBank=[]
        self.obstacle=[]
        self.temporaryBank=[]
        self.bool=True
        if fix==1:
            column=random.randint(0,self.col_input-1)
            self.row_col_fix=["column",self.col_input]
        elif fix==2:
            row=random.randint(0,self.row_input-1)
            self.row_col_fix=["row",self.row_input]
            
        row,column,side=self.side_retry(row,column,side)
        if self.side_count<self.row_col_fix[1]:
            piece=self.ops[side][6][0]
            self.field[row][column]=piece
            self.memoryBank.append([row,column,side,len(self.memoryBank)])
            
            self.check_options(row, column,side)
        
            if self.retry==True:
                self.retry_execute()
        self.side_count=0

    '''checks possible directions of movement'''
    def check_options(self,row,column,side):
        self.retry=False
        options=self.options_create(row,column,side,"options")
        options=self.obstacle_check(row, column, options)
        self.temporary_append()
        if len(options)==0:
            self.no_options()
        if len(self.memoryBank) <=self.wall_length and len(self.memoryBank)!=0 and self.retry==False:
            self.piece_map(row,column,options)
                    
    '''creates possible options based on location'''   
    def options_create(self,row,column,side,value):
        options=self.ops.copy()
        if type(side)==list:
            for i in side:
                del options[i]
        else:
            del options[side]
        options=self.corner_exceptions(row, column, options)
        options,val=self.check_spacing(row, column, options)
        if value=="options":
            return options
        else:
            return val
        
    '''check if piece is near an edge and removes that option'''
    def corner_exceptions(self,row,column,options):
        ops=options.copy()
        if (row==self.row_input-2 or row==self.row_input-1) and "down" in options:
            del ops["down"]
        if (row==1 or row==0) and "up" in options:
            del ops["up"]
        if (column==1 or column==0) and "left" in options:
            del ops["left"]
        if (column==self.col_input-2 or column==self.col_input-1) and "right" in options:
            del ops["right"]
        return ops 
    
    '''checks that pieces are not overlapping or too close together
    returns both possible options and the state val which describes
    if there were any conflicting options present'''    
    def check_spacing(self,row,column,options):
        ops=[]
        val=1
        if options=={}:
            val=0
        for j in options:
            self.bool=True
            for i in range(6):
                try:
                    radd=options[j][i][0]
                    cadd=options[j][i][1]
                    if self.field[row+radd][column+cadd] != " ":
                        self.bool=False
                        val=0
                except IndexError:
                    pass
            if self.bool==True and j not in ops:
                ops.append(j)
        self.bool=True
        return ops,val
    
    '''checks previously failed turns to make sure code does not repeat'''                
    def obstacle_check(self,row,column,options):
        ops=[]
        for i in range(len(options)):
            radd=self.ops[options[i]][1][0]
            cadd=self.ops[options[i]][1][1]
            for j in range(len(self.obstacle)):
                if options[i]==self.obstacle[j][2] and (row+radd)==self.obstacle[j][0] and (column+cadd)==self.obstacle[j][1]:
                    ops.append(options[i])
        for i in range(len(ops)):
            options.remove(ops[i])
        return options               

    '''appends the current largest memoryBank'''
    def temporary_append(self):
        if len(self.memoryBank)>len(self.temporaryBank):
            self.temporaryBank=[]
            for i in range(len(self.memoryBank)):
                self.temporaryBank.append(self.memoryBank[i])
    
    '''function deletes last move and either: tries placing different pieces, 
    sets the wall to start at a different location, or recreates the largest temporary bank'''            
    def no_options(self): 
        side=self.memoryBank_delete()
        if len(self.memoryBank)==0:
            self.retry=True
            if self.side_count>=self.row_col_fix[1]:
                self.temporary_execute()
        else:
            n=len(self.memoryBank)-1
            if self.ops[self.memoryBank[n][2]][7][0] not in side: 
                    side.append(side.append(self.ops[self.memoryBank[n][2]][7][0]))
                    del side[len(side)-1]
                    
            self.check_options(self.memoryBank[n][0],self.memoryBank[n][1],side)
    
    '''deletes latest piece from the memoryBank and returns the direction it went'''
    def memoryBank_delete(self):
        n=len(self.memoryBank)-1
        self.obstacle_append(n)
        side=self.obstacle_translate(n)
        del self.memoryBank[n]
        return side
    
    '''in charge of maps pieces to the map'''    
    def piece_map(self,row,column,options):
            n=random.randint(0,len(options)-1)
            
            for i in self.ops:
                if i==options[n]:
                    radd=self.ops[i][1][0]
                    cadd=self.ops[i][1][1]
                    self.field[row+radd][column+cadd]=self.ops[i][6][0]
                    self.memoryBank.append([row+radd,column+cadd,i,len(self.memoryBank)])
                    self.check_options(row+radd,column+cadd,self.ops[i][7][0])
    
    '''adds premature dead ends to a no go list'''            
    def obstacle_append(self,n):
        self.bool=True
        if len(self.obstacle)==0:
            self.obstacle.append(self.memoryBank[n])
        for i in range(len(self.obstacle)):
            if self.obstacle[i][0]==self.memoryBank[n][0] and self.obstacle[i][1]==self.memoryBank[n][1] and self.obstacle[i][2]==self.memoryBank[n][2] and self.obstacle[i][3]==self.memoryBank[n][3]:
                self.bool=False
        if self.bool==True:
            self.obstacle.append(self.memoryBank[n])

    '''returns all possible failed directions from the no go list for a specific row and column location'''        
    def obstacle_translate(self,n):
        n=len(self.memoryBank)-1
        side=[]
        for i in range(len(self.obstacle)):
            if self.obstacle[i][0]==self.memoryBank[n][0] and self.obstacle[i][1]==self.memoryBank[n][1] and self.obstacle[i][2] not in side:
                side.append(self.obstacle[i][2])
        self.field[self.memoryBank[n][0]][self.memoryBank[n][1]]=" "
        return side
    
    '''recreates the largest memoryBank and maps it to board'''
    def temporary_execute(self):
            self.retry=False
            if self.options_create(self.temporaryBank[0][0],self.temporaryBank[0][1],self.temporaryBank[0][2],"val")==1:
                for i in range(len(self.temporaryBank)):
                    row=self.temporaryBank[i][0]
                    column=self.temporaryBank[i][1]
                    piece=self.ops[self.temporaryBank[i][2]][6][0]
                    self.field[row][column]=piece

    '''retries an edge value if conflicts with spacing'''            
    def side_retry(self,row,column,side):
        val=0
        while val==0 and self.side_count<self.row_col_fix[1]:
            if side=="left" or side=="right":
                row=row+1
            elif side=="up"or side=="down":
                column=column+1
            if row>self.row_input-1:
                row=0
            if column>self.col_input-1:
                column=0
            val=self.options_create(row,column,side,"val")

            self.side_count+=1
            
        return row,column,side
        
    '''continues wall creation process or recalls largest temporaryBank'''
    def retry_execute(self):
        row=self.temporaryBank[0][0]
        column=self.temporaryBank[0][1]
        side=self.temporaryBank[0][2]

        row,column,side=self.side_retry(row,column,side)

        if self.side_count<self.row_col_fix[1]:

            self.wall_create(row,column,3,side)
        else:
            self.temporary_execute()

class Path_Find(Field_Test):
    
    ops=[[0,-1,"left"],[0,1,"right"],[-1,0,"up"],[1,0,"down"]]
    
    
    def __init__(self,row_input,col_input):
        self.row_input=row_input
        self.col_input=col_input
    path_values=[]
    value_cont=[]
    field2=[]
        
    def field_copy(self):
        for i in range(self.row_input):
            row=[]
            for j in range(self.col_input):
                row.append(self.field[i][j])
            self.field2.append(row)

    def transform(self):
        for i in range(self.row_input):
            for j in range(self.col_input):
                if self.field2[i][j]!=" ":
                    self.field2[i][j]=0
    
    def start_end_location(self,diff,loc):
        val=0
        i=0
        exclude="no"
        while val==0:
            row=random.randint(0,self.row_input-1)
            column=random.randint(0,self.col_input-1)
            if self.field2[row][column]!= diff and self.field2[row][column] != "*":
                self.field2[row][column]=loc
                val=1
            i+=1
            if i> self.row_input*self.col_input:
                exclude="yes"
                print "here"
                break
        return row,column,exclude
    
    
    def value_spread(self):
        temp=[]
        for i in range(len(self.value_cont)):
            for j in range(4):
                row=self.value_cont[i][0]+self.ops[j][0]
                column=self.value_cont[i][1]+self.ops[j][1]
                try:
                    if self.field2[row][column]==" " and row>=0 and column>=0:
                        self.field2[row][column]=self.value_cont[i][3]-1
                        temp.append([row,column,self.value_cont[i][2],self.value_cont[i][3]-1])
                except IndexError:
                    pass
        self.value_cont=temp
        if len(self.value_cont)!=0:
            self.value_spread()
    
    def value_start(self):
        row,column,c=self.start_end_location(0,"*")
        self.path_values.append([row,column])
        value=self.row_input*self.col_input
        for i in range(4):
            try:
                if self.field2[row+self.ops[i][0]][column+self.ops[i][1]]==" " and row+self.ops[i][0]>=0 and column+self.ops[i][1]>=0:
                    self.field2[row+self.ops[i][0]][column+self.ops[i][1]]=value
                    self.value_cont.append([row+self.ops[i][0],column+self.ops[i][1],self.ops[i][2],value])
            except IndexError:
                pass
    
    def path(self,row,column):
        value=[]
        for i in range(len(self.ops)):
            try:
                if [row+self.ops[i][0],column+self.ops[i][1]]==self.path_values[0]:
                    value.append(self.field2[row+self.ops[i][0]][column+self.ops[i][1]])
                elif [row+self.ops[i][0],column+self.ops[i][1]] not in self.path_values and row+self.ops[i][0]>=0  and column+self.ops[i][1]>=0:
                    value.append(self.field2[row+self.ops[i][0]][column+self.ops[i][1]])
                else:
                    #print "removed",[row+self.ops[i][0],column+self.ops[i][1]]
                    value.append(0)
                    
                    
            except IndexError:
                value.append(0)
        #print "path val",self.path_values
        if "*" not in value:
            if value!=[0,0,0,0]:
                side=value.index(max(value))
                row=row+self.ops[side][0]
                column=column+self.ops[side][1]
                self.field2[row][column]=":"
                self.path_values.append([row,column])
                #print"chosen",[row,column]
                self.path(row,column)
        
        
        
    def execute(self):
        self.field2=[]
        self.field_copy()
        self.transform()
        self.value_start()
        self.value_spread()
        row,column,exclude=self.start_end_location(0,"+")
        #self.display_field2()
        if exclude=="no":
            self.path_values.append([row,column])
        self.path(row,column)
        self.clean_field()
        self.display_field()

        

    def clean_field(self):
        for i in range(len(self.path_values)):
            if i==0:
                self.field[self.path_values[i][0]][self.path_values[i][1]]="*"
            elif i==1:
                self.field[self.path_values[i][0]][self.path_values[i][1]]="+"
            else:
                self.field[self.path_values[i][0]][self.path_values[i][1]]=":"
        self.path_values=[]
    
    def field2_clear(self):
        for i in range(self.row_input):
            for j in range(self.col_input):
                self.field2[i][j]=" "
                
    def display_field2(self):
        print " -"*self.col_input
        for i in range(self.row_input):
            print "|",
            sys.stdout.write("%s" % self.field2[i][0])
            for j in range(1,self.col_input):
                sys.stdout.write("%4s" % self.field2[i][j])
            sys.stdout.write("|") 
            print
        print " -"*self.col_input
        
    
    
instfieldtest=Field_Test()
instpathfind=Path_Find(instfieldtest.row_input,instfieldtest.col_input)
#for i in range(10):
instfieldtest.field_create()
instfieldtest.set_walls()
instfieldtest.display_field()    
instpathfind.execute()
    #print "next"
    #instfieldtest.field_clear()
    #instpathfind.field2_clear()