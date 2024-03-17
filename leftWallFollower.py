import Senior_Thesis.API as API
import sys

def log(string):
    sys.stderr.write("{}\n".format(string))
    sys.stderr.flush()

def main():
    orient=0
    x,y = 0,0
    API.setColor(0, 0, "G")
    #API.setText(0, 0, "abc")
    while True:
        if not API.wallLeft():
            API.turnLeft()
            orient=API.orientation(orient,'L')
        while API.wallFront():
            API.turnRight()
            orient=API.orientation(orient,'R')
        API.setColor(x, y, "G")
        API.moveForward()
        x,y = API.updateCoordinates(x,y,orient)


if __name__ == "__main__":
    main()