
#function that checks if a value x at position [i,j] is a valid under the sudoku constraints.

def valid(sudoku,i,j,x):
    row=sudoku[i]
    col=sudoku[:,j]

    boxrow=(i//3)*3 #finds the first row of the box. Either 0,3 or 6
    boxcol=(j//3)*3 #finds the first col of the box. Either 0,3 or 6
    box=sudoku[boxrow:boxrow+3][:,boxcol:boxcol+3] #creates the box that x is in

    if x not in row and x not in col and x not in box:
        return True #returns True is number possible under the constraints

#function that finds the next empty square. starting with the top left.
def empty(sudoku):
    empty=[]
    for i in range(0,9):
        for j in range(0,9):
            if sudoku[i][j] == 0:
                empty.append([i,j])
    return empty #returns a list of empty square coordinates



def sudoku_solver(sudoku):
    """
    Solves a Sudoku puzzle and returns its unique solution.

    Input
        sudoku : 9x9 numpy array
            Empty cells are designated by 0.

    Output
        9x9 numpy array of integers
            It contains the solution, if there is one. If there is no solution, all array entries should be -1.
    """


    #initialising lists
    options=[]
    alloptions=[]
    stack=[]
    visited=[]

    #finding all the empty squares
    emptysq=(empty(sudoku))

    #for each empty square, finding all the possible values for that cell under the constraints
    for sq in emptysq:
        i=sq[0]
        j=sq[1]
        options=[[i,j]]
        for x in range(1,10):
            if valid(sudoku,i,j,x):
                options.append(x) #adding each option to the cell

        alloptions.append(options) #adding all cells to the all options list

    foralloptions=alloptions.copy()

    #for each square with its possible options, assign the square
    for option in foralloptions:
        i=option[0][0]
        j=option[0][1]
        coord=option.pop(0)


        for x in option:
            if valid(sudoku,i,j,x): #check if the possible value is valid
                sudoku[i][j]=x #assign the value to the sudoku
                stack.append([coord,option]) #add this cell with all its possibilities to the stack
                visited.append([coord,x]) #add this value to visited
                pass

            else:
                if len(option)==1: #if the option is not valid, and it is the only option
                    completestack=stack.copy()

                    for option in completestack:
                        option=stack.pop() #take the first value from the stack
                        i=option[0][0]
                        j=option[0][1]
                        coord=option.pop(0)
                        option=option.pop() #pop function twice the options were a nested list

                        if len(option)==1: #if there is only one option assign this to 0
                            visited.pop()
                            sudoku[i][j]=0
                        elif len(option)>1: #if there are more than one options

                            for x in option:
                                if [coord,x] in visited: #check if they have been visited
                                    visited.pop()

                                else:
                                    sudoku[i][j]=x #if not visited then assign this value to the sudoku
                                    sudoku_solver(sudoku) #solve the sudoku using this partial value


    #check if row or columns contain any duplicate values
    for i in range(0,9):
        for j in range(0,9):
            row=sudoku[i]
            col=sudoku[:,j]

            duplicatesrow=len(row)!=len(set(row))
            duplicatescol=len(col)!=len(set(col))

            if duplicatesrow or duplicatescol:
                sudoku=np.full((9,9),-1.)

    #if there are any empty squares, return 9x9 array of -1
    emptysq=empty(sudoku)
    if len(emptysq)!=0:
        sudoku=np.full((9,9),-1.)

    return sudoku

