# Read an initial configuration of the puzzle from a file 
def read_puzzle(id):
    with open(id, 'r') as f:
        line = f.read().replace("\n", "")
        return line    

# Check if the value of each blocks are the same:
def check_blocks(lstofblocks, val):
    for block in lstofblocks:
        if block != val: return False
    return True
    
def is_goal(state):
    return check_blocks([state[4*3+1],state[4*3+2],state[4*4+1],state[4*4+2]],'1')
    
def find_empty(state):
    empty = []
    for i in range(5):
        for j in range(4):
            if state[4*i+j] == '0':
                empty.append((i,j))        
    return empty
    
def switch_block(state,i1,j1,i2,j2,val):
    new_state = state.copy()
    new_state[4*i1 + j1] = val
    new_state[4*i2 + j2] = '0'
    
    return new_state

def is_1by2block(state, i, j, val):
    if val not in ['0','1','7'] and state[4*i+j] == val: return True
    return False    

def get_successors(state):
    
    successors = []
    
    # Find empty blocks to move
    empty_blocks = find_empty(state)
    (i0,j0) = empty_blocks[0]
    (i1,j1) = empty_blocks[1]
    
    cur_state = [char for char in state]  

    
    # Switch 1x2 empty block with 1x2, 2x2 blocks
    if (i0 == i1 and j1 == j0+1):
        for delta in [-1,1]:

            # Move up/down to switch 1x2 block
            if (i0+delta >= 0 and i0+delta <= 4):
                val = state[4*(i0+delta) + j0]
                
                if is_1by2block(state,i1+delta,j1,val):
                    new_state=switch_block(cur_state,i0,j0,i0+delta,j0,val)
                    new_state=switch_block(new_state,i1,j1,i1+delta,j1,val)
                    successors.append(''.join(new_state))
                
            # Move up/down to switch 2x2 block
            if (i0+delta*2 >= 0 and i0+delta*2 <=4):
                val = state[4*(i0+delta*2) + j0]
                if check_blocks([state[4*(i0+delta*2) + j1],state[4*(i0+delta) + j0],state[4*(i0+delta) + j1]],val):
                    new_state=switch_block(cur_state,i0,j0,i0+delta*2,j0,val)
                    new_state=switch_block(new_state,i1,j1,i1+delta*2,j1,val)
                    successors.append(''.join(new_state))
                    
        # Move left to switch 1x2 block
        if (j0-2 >= 0):
            val = state[4*i0 + j0 - 1]
            
            if is_1by2block(state, i0, j0-2, val):
                new_state=switch_block(cur_state,i0,j0,i0,j0-2,val)
                successors.append(''.join(new_state))
    
        # Move right to switch 1x2 block
        if (j1+2 <= 3):
            val = state[4*i0 + j1 + 1]
            if state[4*i0 + j1 + 2] == val and val not in  ['0','1','7']: #1x2 block
                new_state=switch_block(cur_state,i1,j1,i1,j1+2,val)
                successors.append(''.join(new_state))


    
    # Switch 2x1 empty block with 2x1, 2x2 blocks
    if (i0 == i1-1 and j0 == j1):
        for delta in [-1,1]:

            # Move left/right to switch 2x1 block
            if (j0+delta >= 0 and j0+delta <= 3):
                val = state[4*i0 + j0+delta]
                if is_1by2block(state, i1,j0+delta, val):
                    new_state=switch_block(cur_state,i0,j0,i0,j0+delta,val)
                    new_state=switch_block(new_state,i1,j1,i1,j1+delta,val)
                    successors.append(''.join(new_state))
                
            # Move left/right to switch 2x2 block
            if (j0+delta*2 >= 0 and j0+delta*2 <=3):
                val = state[4*i0 + j0+delta*2]
                if check_blocks([state[4*i0 + j0+delta],state[4*i1 + j0+delta],state[4*i1 + j0+delta*2]],val):
                    new_state=switch_block(cur_state,i0,j0,i0,j0+delta*2,val)
                    new_state=switch_block(new_state,i1,j1,i1,j1+delta*2,val)
                    successors.append(''.join(new_state))
                
        # Move up to switch 2x1 block
        if (i0-2 >= 0):
            val = state[4*(i0-1) + j0]
            if is_1by2block(state, i0-2, j0, val):
                new_state=switch_block(cur_state,i0,j0,i0-2,j0,val)
                successors.append(''.join(new_state))
    
        # Move down to switch 2x1 block
        if (i1+2 <= 4):
            val = state[4*(i1+1) + j1]
            if is_1by2block(state, i1+2, j1, val):
                new_state=switch_block(cur_state,i1,j1,i1+2,j1,val)
                successors.append(''.join(new_state))
    
    # Switch 1x1 empty block with 1x1, 2x1, 1x2 blocks
    for (i,j) in empty_blocks:
    
        for delta in [-1,1]:

            # Move up/down to switch 1x1 block
            if (i+delta >= 0 and i+delta <= 4):
                val = state[4*(i+delta) + j]
                if val == '7':
                    new_state=switch_block(cur_state,i,j,i+delta,j,val)
                    successors.append(''.join(new_state))

            # Move up/down to switch 2x1 block
            if (i+delta*2 >= 0 and i+delta*2 <=4):
                val = state[4*(i+delta*2) + j]
                if is_1by2block(state, i+delta, j, val):
                    new_state=switch_block(cur_state,i,j,i+delta*2,j,val)
                    successors.append(''.join(new_state))

            # Move left/right to switch 1x1 block
            if (j+delta >= 0 and j+delta <= 3):
                val = state[4*i + j+delta]
                if val == '7':
                    new_state=switch_block(cur_state,i,j,i,j+delta,val)
                    successors.append(''.join(new_state))

            # Move left/right to switch 1x2 block
            if (j+delta*2 >= 0 and j+delta*2 <=3):
                val = state[4*i+ j+delta*2]
                if is_1by2block(state, i, j+delta, val):
                    new_state=switch_block(cur_state,i,j,i,j+delta*2,val)
                    successors.append(''.join(new_state))
    
    return successors
    
    
# every move is a cost of 1 (g value of the state)
def get_cost(path):
    return len(path) - 1


def find_upleft_corner(state):
    for i in range(4):
        for j in range(3):
            if state[4*i + j] == '1':
                return (i,j) 
    
def get_heuristic(state):
    (i1, j1) = find_upleft_corner(state)
    (i2, j2) = (3,1)
    return abs(i1 - i2) + abs(j1 - j2)
    
def print_state(state):
    result = ''
    for i in range(5):
        result += state[4*i]+state[4*i+1]+state[4*i+2]+state[4*i+3]+'\n'
        
    return result




def simplify_state(state):
    simple_state = [char for char in state]  
    for i in range(5):
        for j in range(4):
            val = state[4*i+j]
            if val in ['2','3','4','5','6']:
                if j+1 <= 3 and state[4*i+j+1] == val: # horizontal
                    simple_state[4*i+j] = '8'
                    simple_state[4*i+j+1] = '8'

                if i+1 <= 4 and state[4*(i+1)+j] == val: #vertical
                    simple_state[4*i+j] = '9'
                    simple_state[4*(i+1)+j] = '9' 

    return ''.join(simple_state)

    
# Reference: https://docs.python.org/3/library/queue.html#queue.PriorityQueue
import threading, queue

def a_star(initial_state):
    
    # Variable to keep track of the node expanded
    expanded = 0
    
    # Frontier store the path to the current state directly using PriorityQueue
    frontier = queue.PriorityQueue()    
    frontier.put((0,[initial_state]))
   
    # Keep track of the explored nodes
    explored=[]
    explored.append(simplify_state(initial_state))

    while not frontier.empty():
        
        # the state (current_state) that will be expanded
        current_path = frontier.get()[1]
        current_state = current_path[len(current_path)-1]
        expanded += 1
        
        # Check if the current_state is goal state
        if is_goal(current_state):
            break # we find a goal state
            
        # Investigate Successor States
        for next_state in get_successors(current_state):
    
            simple_state = simplify_state(next_state)

            # Add a new possible path
            if simple_state not in explored:
                priority = get_cost(current_path) + 1 + get_heuristic(simple_state)   
                new_path = current_path.copy()
                new_path.append(next_state)
                frontier.put((priority, new_path))
                explored.append(simple_state)

    return expanded, current_path


def dfs(initial_state):
    
    # Keep track of the node expanded
    expanded = 0
    
    # Frontier store the path to the current state directly using Stack
    frontier = []
    frontier.append([initial_state])
   
    # Keep track of the explored nodes
    explored=[]
    explored.append(simplify_state(initial_state))

    while len(frontier) > 0:
        
        # the state (current_state) that will be expanded
        current_path = frontier.pop()
        current_state = current_path[len(current_path)-1]
        expanded += 1
        
        # Check if the current_state is goal state
        if is_goal(current_state):
            break # we find a goal state
            
        # Investigate Successor States
        for next_state in get_successors(current_state):
    
            simple_state = simplify_state(next_state)

            # Add a new possible path
            if simple_state not in explored:
                new_path = current_path.copy()
                new_path.append(next_state)
                frontier.append(new_path)
                explored.append(simple_state)

    return expanded, current_path

                
def save_file(filename, initial_result, opt_path, expanded):
    with open(filename, 'w') as file:
        file.write("Initial state:\n")
        file.write(initial_result + '\n')
        file.write("Cost of the solution: " + str(get_cost(opt_path)) + '\n\n')
        file.write("Number of states expanded: " + str(expanded) + '\n\n')
        file.write("Solution:\n")
        
        for i in range(len(opt_path)):
            file.write('\n'+ str(i) + '\n')
            file.write(print_state(opt_path[i]))

        file.close()


def astar_solver(id):
    initial_state = read_puzzle(id)
    initial_result = print_state(initial_state)
    expanded, opt_path = a_star(initial_state)
    save_file(id[:-4]+'sol_astar.txt', initial_result, opt_path, expanded)


def dfs_solver(id):
    initial_state = read_puzzle(id)
    initial_result = print_state(initial_state)
    expanded, opt_path = dfs(initial_state)
    save_file(id[:-4]+'sol_dfs.txt', initial_result, opt_path, expanded)
    
if __name__ == "__main__":
    astar_solver('puzzle1.txt')
    astar_solver('puzzle2.txt')
    dfs_solver('puzzle1.txt')
    dfs_solver('puzzle2.txt')
