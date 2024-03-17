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
            
def backtrack():
    global mouse_x, mouse_y
    if path_stack:
       
        path_stack.pop()
        if path_stack:
           
            last_x, last_y = path_stack[-1]
            
            dx = last_x - mouse_x
            dy = last_y - mouse_y
           
            if dx == 1:
                turn_to(EAST)
            elif dx == -1:
                turn_to(WEST)
            elif dy == 1:
                turn_to(NORTH)  
            elif dy == -1:
                turn_to(SOUTH)  
            
            try:
                API.moveForward()
                mouse_x, mouse_y = last_x, last_y
            except API.MouseCrashedError:
                
                API.setColor(mouse_x, mouse_y, 'r')
                API.setText(mouse_x, mouse_y, 'Critical Crash')
                raise


def teversePath(path):
    global mouse_x, mouse_y, path_stack
    while path:
        # Pop the current position, since we're backtracking from here
        path.pop()
        if path:
            # next position to backtrack to
            last_x, last_y = path[-1]
            # Compute the direction to it
            dx = last_x - mouse_x
            dy = last_y - mouse_y
            # Rotate the mouse to face it
            if dx == 1:
                turn_to(EAST)
            elif dx == -1:
                turn_to(WEST)
            elif dy == 1:
                turn_to(NORTH)  
            elif dy == -1:
                turn_to(SOUTH) 
            
            try:
                API.moveForward()
                mouse_x, mouse_y = last_x, last_y
            except API.MouseCrashedError:
                API.setColor(mouse_x, mouse_y, 'r')
                API.setText(mouse_x, mouse_y, 'Critical Crash')
                raise




def turn_to(direction):
    while mouse_dir != direction:
        turn_right()

def dfs_explore(x, y):
    global done
    global goal

    if (x,y) == goal or done==True:
        done=True
        return
    visited.add((x, y))
    API.setColor(x, y, 'g')  # Green for visited
    turn_to(NORTH)
    for d in range(4):
        if is_move_possible():
            if move_forward():
                dfs_explore(mouse_x, mouse_y)
                if done:
                    return 
                  # Backtrack to the previous position after exploring
        
        # Rotate the mouse to explore a new direction
        turn_right()
    
    backtrack()
    dfs_explore(mouse_x, mouse_y)

    
    # Mark backtracking path with a different color (optional)
    API.setColor(x, y, 'y')

def main():
    global visited, path_stack
    visited.clear()  # Clear the visited set in case of reset
    path_stack = [(0, 0)]  # Initialize path stack with the starting position

    # Start the DFS exploration
    dfs_explore(mouse_x, mouse_y)
    copy = list(path_stack)
    teversePath(copy)

    path_stack.reverse()
    teversePath(path_stack)



    API.setColor(mouse_x, mouse_y, 'b')  # Yellow for completion

if __name__ == "__main__":
    main()
