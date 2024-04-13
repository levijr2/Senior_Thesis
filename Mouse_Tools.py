import API
import sys

def showSuroundingWalls(x,y,orient,L,R,F): # highlights walls as they are found
    if(orient==0):
        if(L):
            API.setWall(x,y,'w')
        if(F):
            API.setWall(x,y,'n')
        if(R):
            API.setWall(x,y,'e')
    if(orient==1):
        if(L):
            API.setWall(x,y,'n')
        if(F):
            API.setWall(x,y,'e')
        if(R):
            API.setWall(x,y,'s')

    if(orient==2):
        if(L):
            API.setWall(x,y,'e')
        if(F):
            API.setWall(x,y,'s')
        if(R):
            API.setWall(x,y,'w')
    if(orient==3):
        if(L):
            API.setWall(x,y,'s')
        if(F):
            API.setWall(x,y,'w')
        if(R):
            API.setWall(x,y,'n')

def log(string):
    sys.stderr.write("{}\n".format(string))
    sys.stderr.flush()