#Group Project
import os, random

#board for display purpose. Serve as an upper layer to show to user
#                 A   B   C   D   E   F   G   H   I
displayboard = [['?','?','?','?','?','?','?','?','?'], #row 1
                ['?','?','?','?','?','?','?','?','?'],  #row 2
                ['?','?','?','?','?','?','?','?','?'],  #row 3
                ['?','?','?','?','?','?','?','?','?'],  #row 4
                ['?','?','?','?','?','?','?','?','?'],  #row 5
                ['?','?','?','?','?','?','?','?','?'],  #row 6
                ['?','?','?','?','?','?','?','?','?'],  #row 7
                ['?','?','?','?','?','?','?','?','?'],  #row 8
                ['?','?','?','?','?','?','?','?','?']]  #row 9
#board to record actual state (mine position & surounding numbers)
#                 A   B   C   D   E   F   G   H   I
actualboard = [['?','?','?','?','?','?','?','?','?'], #row 1
                ['?','?','?','?','?','?','?','?','?'],  #row 2
                ['?','?','?','?','?','?','?','?','?'],  #row 3
                ['?','?','?','?','?','?','?','?','?'],  #row 4
                ['?','?','?','?','?','?','?','?','?'],  #row 5
                ['?','?','?','?','?','?','?','?','?'],  #row 6
                ['?','?','?','?','?','?','?','?','?'],  #row 7
                ['?','?','?','?','?','?','?','?','?'],  #row 8
                ['?','?','?','?','?','?','?','?','?']]  #row 9

win = False
lose = False
mine_count = 0
emptycell_lst = []
checked_lst = []
colref = {"a":0,"b":1,"c":2,"d":3,"e":4,"f":5,"g":6,"h":7,"i":8} #dictionary to translate column letter to index

def debugcheck(input_action="",board=actualboard):
    #only active if input action is "d"
    #prints actual board and end program
    if input_action.lower() == "d":
        print("")
        print("")
        print("")
        print("Debug Mode - Actual board showcase: ")
        printscreen(board)

def printscreen(board):
    #A function to print the desired board out.
    print("    A  B  C  D  E  F  G  H  I")
    for i in range(len(board)):
        sentence = ""
        sentence += str(i+1) + "|"
        for j in range(len(board[i])):
            sentence += "  " + str(board[i][j])
        print(sentence + "  |" + str(i+1))

def flag(col,row,fakeboard,outputscreen=False):
    #col, row = user input
    #fakeboard = board to display (flag interacts with the display screen only)
    #outputscreen = option to print screen
    colindex = colref.get(col.lower())
    rowindex = row - 1
    #Case 1 - add flag to hidden cells
    if fakeboard[rowindex][colindex] == "?":
        fakeboard[rowindex][colindex] = "F"
    #Case 2 - remove flag from flagged cells
    elif fakeboard[rowindex][colindex] == "F":
        fakeboard[rowindex][colindex] = "?"
    #Case 3 - error if cell is already uncovered
    else:
        print("Error")

    #Clear screen and print update board if outputscreen option is True
    if outputscreen:
        if not win and not lose:
            os.system("cls")
            print("Action detected, there is the updated board.")
            printscreen(displayboard)

def empty_scanner(vcol,vrow,col_offset,row_offset,fakeboard,realboard):
    global emptycell_lst, checked_lst
    newrow = vrow + row_offset
    newcol = vcol + col_offset
    if not (0 <= newrow < len(realboard)) or not (0 <= newcol < len(realboard)):
        return
    checked_lst.append((newrow,newcol))
    while realboard[newrow][newcol] == " ":
        emptycell_lst.append((newrow,newcol))
        newrow += row_offset
        newcol += col_offset
        if not (0 <= newrow < len(realboard)) or not (0 <= newcol < len(realboard)):
            return

def uncover(col,row,fakeboard,realboard,outputscreen=False):
    #col, row = user input
    #fakeboard = board to display
    #realboard = board that record actual state
    #outputscreen = option to print screen
    global win, lose, emptycell_lst, checked_lst
    emptycell_lst = []
    checked_lst = []
    colindex = colref.get(col.lower())
    rowindex = row - 1
    clear = False

    #update fake board cell status with real board cell status
    if fakeboard[rowindex][colindex] != "F":
        fakeboard[rowindex][colindex] = realboard[rowindex][colindex]
    #or end this function to prevent uncovering a flagged cell
    else:
        print("Hey! That block could be dangerous.")
        print("We have prevented you from uncovering a flagged cell. :>")
        return

    #spread
    #1.find all empty cells in surrounding first
    #scan empty cells in 8 directions
    empty_scanner(colindex,rowindex,-1,0,displayboard,actualboard) #west
    empty_scanner(colindex,rowindex,-1,-1,displayboard,actualboard) #north west
    empty_scanner(colindex,rowindex,0,-1,displayboard,actualboard) #north
    empty_scanner(colindex,rowindex,1,-1,displayboard,actualboard) #north east
    empty_scanner(colindex,rowindex,1,0,displayboard,actualboard) #east
    empty_scanner(colindex,rowindex,1,1,displayboard,actualboard) #south east
    empty_scanner(colindex,rowindex,0,1,displayboard,actualboard) #south
    empty_scanner(colindex,rowindex,-1,1,displayboard,actualboard) #south west

    #2.Preparation for second round of checking: dicovered cells minus checked cells
    result = []
    for i in range(len(emptycell_lst)):
        if emptycell_lst[i] not in checked_lst:
            result.append(emptycell_lst[i])

    #3. Repeat step 1 and 2 until all connections has been found
    #Choose to loop 4 times because 3 is not enough but 5 or higher may CRASH the game
    for i in range(4):
        for i in result:
            empty_scanner(i[1],i[0],-1,0,displayboard,actualboard) #west
            empty_scanner(i[1],i[0],-1,-1,displayboard,actualboard) #north west
            empty_scanner(i[1],i[0],0,-1,displayboard,actualboard) #north
            empty_scanner(i[1],i[0],1,-1,displayboard,actualboard) #north east
            empty_scanner(i[1],i[0],1,0,displayboard,actualboard) #east
            empty_scanner(i[1],i[0],1,1,displayboard,actualboard) #south east
            empty_scanner(i[1],i[0],0,1,displayboard,actualboard) #south
            empty_scanner(i[1],i[0],-1,1,displayboard,actualboard) #south west
        result = []
        for i in range(len(emptycell_lst)):
            if emptycell_lst[i] not in checked_lst:
                result.append(emptycell_lst[i])

    #reveal recorded empty empty cells
    for i in emptycell_lst:
        #reveal itself
        fakeboard[i[0]][i[1]] = realboard[i[0]][i[1]]
        #and also reveal surrounding if it is a number
        #axis = offseted index value for 8 directions
        axis = [(i[0]-1,i[1]-1),(i[0]-1,i[1]),(i[0]-1,i[1]+1),(i[0],i[1]-1),
                (i[0],i[1]+1),(i[0]+1,i[1]-1),(i[0]+1,i[1]),(i[0]+1,i[1]+1)]
        for a in axis:
            if 0 <= a[0] < len(realboard[0]) and 0 <= a[1] < len(realboard[0]):
                if realboard[a[0]][a[1]] != "*":
                    fakeboard[a[0]][a[1]] = realboard[a[0]][a[1]]

    #Lose Condition Detection
    #Must be put before win condition checking
    if realboard[rowindex][colindex] == "*":
        lose = True
        os.system("cls")
        print("!    Oops    !")
        printscreen(actualboard)
        print("    !!!!!!!!!!!!!!!!!!!!!!!!!")
        print("You have found a mine! You lose :(")
        print("    !!!!!!!!!!!!!!!!!!!!!!!!!")
        return lose #to exit the uncover function

    #Win Condition Checking
    win_condition_counter = 0
    win_condition_requirement = 81 - mine_count

    for i in range(len(fakeboard)):
        for j in range(len(fakeboard[i])):
            #loop through every single cells to check if cells are uncovered
            if fakeboard[i][j] == realboard[i][j]:
                win_condition_counter += 1
    if win_condition_counter == win_condition_requirement:
        print("Win") #yeah
        win = True
        return win #to exit the uncover function

    #Clear screen and print update board if outputscreen option is True
    if outputscreen:
        os.system("cls")
        print("Action detected, there is the updated board.")
        printscreen(displayboard)

def addmines(minenum,board,startcol,startrow):
    #startcol & startindex to prevent mine spawn kill the player
    startcolindex = colref.get(startcol.lower())
    startrowindex = startrow - 1
    for i in range(minenum):
        #randomize position, find valid cells and assign numbers
        colindex = random.randint(0,8)
        rowindex = random.randint(0,8)
        while board[rowindex][colindex] == "*" or (colindex == startcolindex and rowindex == startrowindex):
            colindex = random.randint(0,8)
            rowindex = random.randint(0,8)
            #loop breaks only if position is valid
            if board[rowindex][colindex] != "*" and not (colindex == startcolindex and rowindex == startrowindex):
                break
        board[rowindex][colindex] = "*"
    return minenum #to update mine_counter variable

def numberupdate(board):
    for i in range(len(board)): #loop each row
        for j in range(len(board[i])): #loop each item(as columns) in row
            counter = 0
            if board[i][j] != "*":
                #extract index of suroundings when the cell is not a mine
                checklst = [(i-1,j-1),(i-1,j),(i-1,j+1),(i,j-1),
                            (i,j+1),(i+1,j-1),(i+1,j),(i+1,j+1)]
                #count surounding mines
                for k in checklst:
                    #fliter invalid surrounding cells (like corner-1, out of index etc)
                    if 0 <= k[0] < len(board[0]) and 0 <= k[1] < len(board[0]):
                        if board[k[0]][k[1]] == "*":
                            counter += 1
                #assign number to cell
                board[i][j] = counter
                #assign blank if no mine nearby
                if board[i][j] == 0:
                    board[i][j] = " "

#main thread
print("Welcome to Minesweeper!")
startmode = input("Press Any to play or \"I\" for Instructions: ")
if startmode.upper() == "I":
    print("===Instructions===")
    input("Press Any to start to play: ")
    printscreen(displayboard)
else:
    printscreen(displayboard)

#First Action
print("Please Uncover a cell as your first move.")
input_col = input("Column? (A~I) :")
input_row = int(input("Row? (1~9) :"))

#generate Mines & store amount of mines in mine_count variable
mine_count = addmines(10,actualboard,input_col,input_row)
numberupdate(actualboard)
uncover(input_col,input_row,displayboard,actualboard)

#remaining GAME LOOP until win or lose
printscreen(displayboard)
while not win or not lose:
    input_action = ""
    while input_action not in ["u","f"]:
        input_action = input("Action (u/f): ").strip()
        debugcheck(input_action,actualboard)
    input_col = input("Column? (A~I) :")
    input_row = int(input("Row? (1~9) :"))
    #Uncover - call uncover()
    if input_action.lower() == "u":
        #uncover cells
        uncover(input_col,input_row,displayboard,actualboard,True)
        #check win/lose
        pass
    #Flag - call flag()
    elif input_action.lower() == "f":
        flag(input_col,input_row,displayboard,True)
