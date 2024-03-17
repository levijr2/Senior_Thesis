import Senior_Thesis.API as API
import sys

def log(string):
    sys.stderr.write("{}\n".format(string))
    sys.stderr.flush()


# Define directions
NORTH, EAST, SOUTH, WEST = range(4)

# Direction vectors for moving (N, E, S, W)
directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

# Initial mouse state
mouse_x, mouse_y = 0, 0  # Starting at (0, 0)
mouse_dir = NORTH  # Starting direction is north
done = False
goal = (API.mazeWidth()//2, API.mazeHeight()//2)

# Track visited cells and the path
visited = set()
path_stack = []

def turn_right():
    global mouse_dir
    API.turnRight()
    mouse_dir = (mouse_dir + 1) % 4

def turn_left():
    global mouse_dir
    API.turnLeft()
    mouse_dir = (mouse_dir - 1) % 4

def move_forward():
    global mouse_x, mouse_y
    dx, dy = directions[mouse_dir]
    new_x, new_y = mouse_x + dx, mouse_y + dy
    if (new_x, new_y) in visited:
        # Already visited this cell; don't move forward
        return False
    try:
        API.moveForward()
        mouse_x, mouse_y = new_x, new_y
        visited.add((mouse_x, mouse_y))
        path_stack.append((mouse_x, mouse_y))  # Add to path
        return True
    except API.MouseCrashedError:
        # Handle crash: mark the cell as a wall and return False
        API.setColor(new_x, new_y, 'r')
        API.setText(new_x, new_y, 'Crash')
        return False

def is_move_possible():
    if (mouse_dir)%4==0:
        dx = mouse_x
        dy = mouse_y+1
    if (mouse_dir)%4==1:
        dx = mouse_x+1
        dy = mouse_y
    if (mouse_dir)%4==2:
        dx = mouse_x
        dy = mouse_y-1
    if (mouse_dir)%4==3:
        dx = mouse_x-1
        dy = mouse_y

    wall = API.wallFront()

    if wall or (dx,dy) in visited:
        return False    
    else:
        return True

def is_move_possible_right():
    if (mouse_dir)%4==0:
        dx = mouse_x+1
        dy = mouse_y
    if (mouse_dir)%4==1:
        dx = mouse_x
        dy = mouse_y-1
    if (mouse_dir)%4==2:
        dx = mouse_x-1
        dy = mouse_y
    if (mouse_dir)%4==3:
        dx = mouse_x
        dy = mouse_y+1

    wall = API.wallRight()

    if wall or (dx,dy) in visited:
        return False    
    else:
        return True

def is_move_possible_left():
    if (mouse_dir)%4==0:
        dx = mouse_x-1
        dy = mouse_y
    if (mouse_dir)%4==1:
        dx = mouse_x
        dy = mouse_y+1
    if (mouse_dir)%4==2:
        dx = mouse_x+1
        dy = mouse_y
    if (mouse_dir)%4==3:
        dx = mouse_x
        dy = mouse_y-1

    wall = API.wallLeft()

    if wall or (dx,dy) in visited:
        return False    
    else:
        return True

def showSuroundingWalls(x,y,orient,L,R,F):
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




def backtrack():
    global mouse_x, mouse_y
    if path_stack:
        # Pop the current position, since we're backtracking from here
        path_stack.pop()
        if path_stack:
            # Peek at the next position to backtrack to
            last_x, last_y = path_stack[-1]
            # Compute the direction to the last position
            dx = last_x - mouse_x
            dy = last_y - mouse_y
            # Rotate the mouse to face the last position    
            if dx == 1:
                turn_to(EAST)
            elif dx == -1:
                turn_to(WEST)
            elif dy == 1:
                turn_to(NORTH)  # Notice this was previously NORTH
            elif dy == -1:
                turn_to(SOUTH)  # Notice this was previously SOUTH
            # Move to the last position
            try:
                API.moveForward()
                mouse_x, mouse_y = last_x, last_y
            except API.MouseCrashedError:
                # If there's a crash while backtracking, it's a critical error
                API.setColor(mouse_x, mouse_y, 'r')
                API.setText(mouse_x, mouse_y, 'Critical Crash')
                raise


def traversePath(path):
    global mouse_x, mouse_y, path_stack
    while path:
        # Pop the current position, since we're backtracking from here
        path.pop()
        if path:
            # Peek at the next position to backtrack to
            last_x, last_y = path[-1]
            # Compute the direction to the last position
            dx = last_x - mouse_x
            dy = last_y - mouse_y
            # Rotate the mouse to face the last position
            if dx == 1:
                turn_to(EAST)
            elif dx == -1:
                turn_to(WEST)
            elif dy == 1:
                turn_to(NORTH)  # Notice this was previously NORTH
            elif dy == -1:
                turn_to(SOUTH)  # Notice this was previously SOUTH
            # Move to the last position
            try:
                API.moveForward()
                mouse_x, mouse_y = last_x, last_y
            except API.MouseCrashedError:
                # If there's a crash while backtracking, it's a critical error
                API.setColor(mouse_x, mouse_y, 'r')
                API.setText(mouse_x, mouse_y, 'Critical Crash')
                raise




def turn_to(direction):
    while mouse_dir != direction:
        #log(mouse_dir)
        #log(direction)
        #log(abs(mouse_dir - direction))
        if(mouse_dir == NORTH and direction==EAST):
            turn_right()
        elif(mouse_dir == NORTH and direction==WEST):
            turn_left()
        elif(mouse_dir == SOUTH and direction==EAST):
            turn_left()
        elif(mouse_dir == SOUTH and direction==WEST):
            turn_right()
        elif(mouse_dir == EAST and direction==SOUTH):
            turn_right()
        elif(mouse_dir == EAST and direction==NORTH):
            turn_left()
        elif(mouse_dir == WEST and direction==SOUTH):
            turn_left()
        elif(mouse_dir == WEST and direction==NORTH):
            turn_right()
        elif( (  abs((mouse_dir - direction))) == 2 ): #this handles 180's
            turn_right()
            turn_right()

        

def dfs_explore(x, y):
    global done
    global goal
    L=API.wallLeft()
    R=API.wallRight()
    F=API.wallFront()
    if (x,y) == goal or done==True:
        done=True
        return
    visited.add((x, y))
    API.setColor(x, y, 'G')  # Green for visited
    # for d in range(4):
    showSuroundingWalls(x,y,mouse_dir,L,R,F)
    if mouse_dir == NORTH:
        if is_move_possible():
            if move_forward():
                dfs_explore(mouse_x, mouse_y)
                if done:
                    return 
        elif is_move_possible_right():
            turn_right()
            if move_forward():
                dfs_explore(mouse_x, mouse_y)
                if done:
                    return
        elif is_move_possible_left():
            turn_left()
            if move_forward():
                dfs_explore(mouse_x, mouse_y)
                if done:
                    return
        
        # elif is_move_possible_back():
        #     turn_right()
        #     turn_right()
        #     if move_forward():
        #         dfs_explore(mouse_x, mouse_y)
        #         if done:
        #             return        


    if mouse_dir == EAST:

        if is_move_possible_left():
            turn_left()
            if move_forward():
                dfs_explore(mouse_x, mouse_y)
                if done:
                    return

        elif is_move_possible():
            if move_forward():
                dfs_explore(mouse_x, mouse_y)
                if done:
                    return
                 
        elif is_move_possible_right():
            turn_right()
            if move_forward():
                dfs_explore(mouse_x, mouse_y)
                if done:
                    return
        # elif is_move_possible_left():
        #     turn_left()
        #     if move_forward():
        #         dfs_explore(mouse_x, mouse_y)
        #         if done:
        #             return
        
        # elif is_move_possible_back():
        #     turn_right()
        #     turn_right()
        #     if move_forward():
        #         dfs_explore(mouse_x, mouse_y)
        #         if done:
        #             return        


    if mouse_dir == SOUTH:

        if is_move_possible_left():
            turn_left()
            if move_forward():
                dfs_explore(mouse_x, mouse_y)
                if done:
                    return

        elif is_move_possible():
            if move_forward():
                dfs_explore(mouse_x, mouse_y)
                if done:
                    return 
        elif is_move_possible_right():
            turn_right()
            if move_forward():
                dfs_explore(mouse_x, mouse_y)
                if done:
                    return
        


    if mouse_dir == WEST:

        if is_move_possible_right():
            turn_right()
            if move_forward():
                dfs_explore(mouse_x, mouse_y)
                if done:
                    return

        elif is_move_possible_left():
            turn_left()
            if move_forward():
                dfs_explore(mouse_x, mouse_y)
                if done:
                    return

        elif is_move_possible():
            if move_forward():
                dfs_explore(mouse_x, mouse_y)
                if done:
                    return 


                # Backtrack to the previous position after exploring
    backtrack()
    dfs_explore(mouse_x, mouse_y)

    
    # Mark backtracking path with a different color (optional)
    #API.setColor(x, y, 'g')

def main():
    global visited, path_stack
    visited.clear()  # Clear the visited set in case of reset
    path_stack = [(0, 0)]  # Initialize path stack with the starting position

    # Start the DFS exploration
    dfs_explore(mouse_x, mouse_y)
    copy = list(path_stack)
    for i in copy:
        API.setColor(i[0], i[1], 'g')
    traversePath(copy)

    path_stack.reverse()
    traversePath(path_stack)




    # Finalization code here
    #API.setColor(mouse_x, mouse_y, 'b')  #dark green
if __name__ == "__main__":
    main()
