from random import randint
import time

gameTurn = "white"
def gameTurnComplete():
    global gameTurn
    if gameTurn == "white":
        gameTurn = "black"
    elif gameTurn == "black":
        gameTurn = "white"

hor_rows = [[1, 2, 3, 4, 5, 6, 7, 8],
    [9, 10, 11, 12, 13, 14, 15, 16],
    [17, 18, 19, 20, 21, 22, 23, 24],
    [25, 26, 27, 28, 29, 30, 31, 32],
    [33, 34, 35, 36, 37, 38, 39, 40],
    [41, 42, 43, 44, 45, 46, 47, 48],
    [49, 50, 51, 52, 53, 54, 55, 56],
    [57, 58, 59, 60, 61, 62, 63, 64]]

#For pawn taking logic.
right_edge = [9, 17, 25, 33, 41, 49, 57]
left_edge = [8, 16, 24, 32, 40, 48, 56, 64]
#For knight and king logic to prevent "pac-manning".
outer_left = [8, 16, 32, 40, 48, 56, 64]
left = [7, 15, 23, 31, 39, 47, 55, 63]
right = [2, 10, 18, 26, 34, 42, 50, 58]
outer_right = [1, 9, 17, 25, 33, 41, 49, 57]
outer2_bot = [1, 2, 3, 4, 5, 6, 7, 8]
outer_bot = [9, 10, 11, 12, 13, 14, 15, 16]
outer_top = [49, 50, 51, 52, 53, 54, 55, 56]
outer2_top = [57, 58, 59, 60, 61, 62, 63, 64]

class WhitePawn():
    def __init__(self, team, name, pos):
        self.team = team
        self.name = name
        self.pos = pos
        self.symbol = "♙"
        
        self.doublemove = True
        self.moves = [] #Psuedo-legal moves that can be made.

    def moveGeneration(self):
        if self.team == "white":

            in_left = False
            in_right = False
            #For single move (since pawns can't take head on regardless).
            holder1 = self.pos + 8
            occupancy1 = False
            for i in pieces:
                if holder1 == i.pos:
                    occupancy1 = True
            if occupancy1 == False:
                self.moves.append(self.pos + 8)
            #For pawn taking logic.
            for i in left_edge:
                if i == self.pos:
                    in_left = True
            for i in right_edge:
                if i == self.pos:
                    in_right = True
                    
            #Since pawns only can either be in left_edge, right_edge, or neither.
            left_take = self.pos + 9
            right_take = self.pos + 7
            if in_left == True:
                for i in pieces:
                    if i.pos == right_take:
                        self.moves.append(right_take) 
            if in_right == True:
                for i in pieces:
                    if i.pos == left_take:
                        self.moves.append(left_take)
            if in_right == False and in_left == False:
                for i in pieces:
                    if i.pos == right_take:
                        self.moves.append(right_take)
                for i in pieces:
                    if i.pos == left_take:
                        self.moves.append(left_take) 

            #For pawn double move.
            if self.pos < 16:
                self.doublemove = True
            holder = self.pos + 16
            occupancy = False
            if self.doublemove == True:
                for i in pieces:
                    if holder == i.pos:
                        occupancy = True
                if occupancy == False and self.pos <= 16:
                    self.moves.append(self.pos + 16)
                    self.doublemove = False
                    
            #Not sure why but had to throw this check in their because moves kept generating 65
            #aka the int set to a piece taken.
            for i in self.moves:
                if i < 0 or i > 64:
                    self.moves.remove(i)

#Opposite math from white pawns.
class BlackPawn():
    def __init__(self, team, name, pos):
        self.team = team
        self.name = name
        self.pos = pos
        self.symbol = "♟"
        self.doublemove = True
        self.moves = []

    def moveGeneration(self):
        if self.team == "black":
            in_left = False
            in_right = False
            holder1 = self.pos - 8
            occupancy1 = False
            for i in pieces:
                if holder1 == i.pos:
                    occupancy1 = True
            if occupancy1 == False:
                self.moves.append(self.pos - 8)

            for i in left_edge:
                if i == self.pos:
                    in_right = True
            for i in right_edge:
                if i == self.pos:
                    in_left = True
                    
            left_take = self.pos - 9
            right_take = self.pos - 7
            if in_left == True:
                for i in pieces:
                    if i.pos == right_take:
                        self.moves.append(right_take) 
            if in_right == True:
                for i in pieces:
                    if i.pos == left_take:
                        self.moves.append(left_take)

            if self.pos >= 49:
                self.doublemove = True
            holder = self.pos - 16
            occupancy = False
            if self.doublemove == True:
                for i in pieces:
                    if holder == i.pos:
                        occupancy = True
                if occupancy == False and self.pos >= 49:
                    self.moves.append(self.pos - 16)
                    
            for i in self.moves:
                if i < 0 or i > 64:
                    self.moves.remove(i)

class Rook():
    def __init__(self, team, name, pos):
        self.name = name
        self.pos = pos
        self.team = team
        if self.team == "white":
            self.symbol = "♖"
        elif self.team == "black":
            self.symbol = "♜"
        self.moves = []
        castleAccess = True #For king to castle to a chosen unmoved rook.
    
    #Adds moves while taking into consideration of current piece pos in "pieces".
    def moveGeneration(self):
        #Indexing the location of piece to allow for movement generation stemming from position on hor_rows 2D array.
        for i in hor_rows:
            for item in i:
                if item == self.pos:
                    intex1 = hor_rows.index(i)
                    itemtex1 = i.index(item)
                    #intex values
                    reset_intex1 = intex1
                    intex_up1 = 8 - intex1
                    intex_down1 = intex1
                    #itemtex values
                    reset_itemtex1 = itemtex1
                    itemtex_right1 = itemtex1
                    itemtex_left1 = 8 - itemtex1

        #Vertical Up
        lopbol = True
        count = 0
        while count < intex_up1 and lopbol == True:
            intex1 += 1
            try: 
                self.moves.append(hor_rows[intex1][itemtex1])
            except:
                break
            for i in pieces:
                if hor_rows[intex1][itemtex1] == i.pos:
                    lopbol = False
                    check_pos = hor_rows[intex1][itemtex1]
                    for piece in pieces:
                        if piece.pos == check_pos:
                            if piece.team == self.team:
                                self.moves.remove(check_pos)
            count += 1

        #Vertical Down
        lopbol = True
        count = 0
        intex1 = reset_intex1
        while count < intex_down1 and lopbol == True:
            intex1 -= 1
            try: 
                self.moves.append(hor_rows[intex1][itemtex1])
            except:
                break
            for i in pieces:
                if hor_rows[intex1][itemtex1] == i.pos:
                    lopbol = False
                    check_pos = hor_rows[intex1][itemtex1]
                    for piece in pieces:
                        if piece.pos == check_pos:
                            if piece.team == self.team:
                                self.moves.remove(check_pos)
            count += 1

        #Horizontal Left
        count = 0
        lopbol = True
        intex1 = reset_intex1
        while count < itemtex_left1 and lopbol == True:
            itemtex1 += 1
            try: 
                self.moves.append(hor_rows[intex1][itemtex1])
            except:
                break
            for i in pieces:
                if hor_rows[intex1][itemtex1] == i.pos:
                    lopbol = False
                    check_pos = hor_rows[intex1][itemtex1]
                    for piece in pieces:
                        if piece.pos == check_pos:
                            if piece.team == self.team:
                                self.moves.remove(check_pos)
            count += 1

        #Horizontal Right
        count = 0
        lopbol = True
        itemtex1 = reset_itemtex1
        while count < itemtex_right1 and lopbol == True:
            itemtex1 -= 1
            try: 
                self.moves.append(hor_rows[intex1][itemtex1])
            except:
                break
            for i in pieces:
                if hor_rows[intex1][itemtex1] == i.pos:
                    lopbol = False
                    check_pos = hor_rows[intex1][itemtex1]
                    for piece in pieces:
                        if piece.pos == check_pos:
                            if piece.team == self.team:
                                self.moves.remove(check_pos)
            count += 1

class Knight():
    def __init__(self, team, name, pos):
        self.name = name
        self.pos = pos
        self.team = team
        if self.team == "white":
            self.symbol = "♘"
        elif self.team == "black":
            self.symbol = "♞"
        self.moves = []

    def moveGeneration(self):
        #Psuedo-legal moves.
        up_left = self.pos + 17
        left_up = self.pos + 10
        left_down = self.pos - 6
        down_left = self.pos - 15

        up_right = self.pos + 15
        right_up = self.pos + 6
        right_down = self.pos - 10
        down_right = self.pos - 17

        self.moves.append(up_left)
        self.moves.append(left_up)
        self.moves.append(left_down)
        self.moves.append(down_left)

        self.moves.append(up_right)
        self.moves.append(right_up)
        self.moves.append(right_down)
        self.moves.append(down_right)

        #Removing the illegal moves based on self-move logic.
        if self.pos in outer_left:
            try:
                self.moves.remove(up_left)
                self.moves.remove(left_up)
                self.moves.remove(left_down)
                self.moves.remove(down_left)
            except:
                pass

        if self.pos in left:
            try:
                self.moves.remove(left_up)
                self.moves.remove(left_down)
            except:
                pass    
        
        if self.pos in right:
            try:
                self.moves.remove(right.up)
                self.moves.remove(right_down)
            except:
                pass

        if self.pos in outer_right:
            try:
                self.moves.remove(up_right)
                self.moves.remove(right_up)
                self.moves.remove(right_down)
                self.moves.remove(down_right)
            except:
                pass

        if self.pos in outer2_bot:
            try:
                self.moves.remove(down_left)
                self.moves.remove(down_right)
                self.moves.remove(right_down)
                self.moves.remove(left_down)
            except:
                pass

        if self.pos in outer_bot:
            try:
                self.moves.remove(down_left)
                self.moves.remove(down_right)
            except:
                pass

        if self.pos in outer_top:
            try:
                self.moves.remove(up_left)
                self.moves.remove(up_right)
            except:
                pass
        
        if self.pos in outer2_top:
            try:
                self.moves.remove(up_left)
                self.moves.remove(up_right)
                self.moves.remove(right_up)
                self.moves.remove(left_up)
            except:
                pass

        #Iffy invalid move reduction. Haha
        for i in self.moves:
            if i < 0:
                self.moves.remove(i)
            if i > 64:
                self.moves.remove(i)
            
class Bishop():
    def __init__(self, team, name, pos):
        self.name = name
        self.pos = pos
        self.team = team
        if self.team == "white":
            self.symbol = "♗"
        elif self.team == "black":
            self.symbol = "♝"
        self.moves = []

    #Locating pos/index in horizontal rows then adding int to find the next diagnoal pos relative to its start.
    def moveGeneration(self):
        #Capturing position to make moves relative to starting pos.
        for i in hor_rows:
            for item in i:
                if item == self.pos:
                    intex = hor_rows.index(i)
                    itemtex = i.index(item)
                    #intex values
                    reset_intex = intex
                    intex_down = intex
                    intex_up = 7 - intex
                    #itemtex values
                    reset_itemtex = itemtex
                    itemtex_right = itemtex
                    intex_down2 = intex_down

        #Diagonal Up-Left
        count = 0
        lopbol = True
        while count < intex_up and lopbol == True:
            itemtex += 1
            intex += 1

            try:
                self.moves.append(hor_rows[intex][itemtex])
            except:
                break
            for i in pieces:
                if hor_rows[intex][itemtex] == i.pos:
                    lopbol = False
            count += 1

        #Diagonal Down-Right 
        count = 0
        lopbol = True
        itemtex = reset_itemtex
        intex  = reset_intex
        while count < intex_down and lopbol == True:
            itemtex -= 1
            intex -= 1

            try:
                self.moves.append(hor_rows[intex][itemtex])
            except:
                break
            for i in pieces:
                if hor_rows[intex][itemtex] == i.pos:
                    lopbol = False
            count += 1

        #Diagonal Up-Right
        count = 0
        lopbol = True
        intex = reset_intex
        itemtex = reset_itemtex
        while count < itemtex_right and lopbol == True:
            itemtex -= 1
            intex += 1

            try:
                self.moves.append(hor_rows[intex][itemtex])
            except:
                break
            for i in pieces:
                if hor_rows[intex][itemtex] == i.pos:
                    lopbol = False
            count += 1

        #Diagonal Down-Left
        count = 0
        lopbol = True
        intex = reset_intex
        itemtex = reset_itemtex
        while count < intex_down2 and lopbol == True:
            itemtex += 1
            intex -= 1

            try:
                self.moves.append(hor_rows[intex][itemtex])
            except:
                break

            for i in pieces:
                if hor_rows[intex][itemtex] == i.pos:
                    lopbol = False
            count += 1

#Checking for self.king in check.
def kingCheck(self):
    #No queen since redundant. Just gonna use bishop or rook "AND" for the checks.
    rookCheck = False
    bishopCheck = False
    knightCheck = False
    pawnCheck = False

    if self.team == "white":
        for pot_check in self.rook_check:
            for piece in pieces:
                if pot_check == piece.pos:
                    if piece.name == "brook1" or piece.name == "brook2" or piece.name == "bquen":
                        rookCheck = True

        for pot_check in self.bishop_check:
            for piece in pieces:
                if pot_check == piece.pos:
                    if piece.name == "bbishop1" or piece.name == "bbishop2" or piece.name == "bquen":
                        bishopCheck = True
        
        for pot_check in self.knight_check:
            for piece in pieces:
                if pot_check == piece.pos:
                    if piece.name == "bknight1" or piece.name == "bknight2":
                        knightCheck = True

        for pot_check in self.pawn_check:
            for piece in pieces:
                if pot_check == piece.pos:
                    if piece.name == "bpawn1" or piece.name == "bpawn2" or piece.name == "bpawn3" or piece.name == "bpawn4" or piece.name == "bpawn5" or piece.name == "bpawn6" or piece.name == "bpawn6" or piece.name == "bpawn7" or piece.name == "bpawn8":
                        pawnCheck = True

        if rookCheck or bishopCheck or knightCheck or pawnCheck:
            return True
        
    if self.team == "black":
        for pot_check in self.rook_check:
            for piece in pieces:
                if pot_check == piece.pos:
                    if piece.name == "wrook1" or piece.name == "wrook2" or piece.name == "wquen":
                        rookCheck = True

        for pot_check in self.bishop_check:
            for piece in pieces:
                if pot_check == piece.pos:
                    if piece.name == "wbishop1" or piece.name == "wbishop2" or piece.name == "wquen":
                        bishopCheck = True
        
        for pot_check in self.knight_check:
            for piece in pieces:
                if pot_check == piece.pos:
                    if piece.name == "wknight1" or piece.name == "wknight2":
                        knightCheck = True

        for pot_check in self.pawn_check:
            for piece in pieces:
                if pot_check == piece.pos:
                    if piece.name == "wpawn1" or piece.name == "wpawn2" or piece.name == "wpawn3" or piece.name == "wpawn4" or piece.name == "wpawn5" or piece.name == "wpawn6" or piece.name == "wpawn6" or piece.name == "wpawn7" or piece.name == "wpawn8":
                        pawnCheck = True

        if rookCheck or bishopCheck or knightCheck or pawnCheck:
            return True

class King():
    #Think of king as a queen but can only make a single move.
    def __init__(self, team, name, pos):
        self.name = name
        self.pos = pos
        self.team = team
        self.canCastle = True
        if self.team == "white":
            self.symbol = "♔"
        elif self.team == "black":
            self.symbol = "♚"
        self.moves = []
        self.rook_check = [] #List of all moves that could be made by any would-be attacker.
        self.knight_check = []
        self.bishop_check = []
        self.pawn_check = []
        
    #going to reverse all legal moves from this pos to determine if there is an 
    #adaquate piece that would therefore be rendering a check. Also to prevent 
    #moving into check and to determie check/stale mate.
    def checkMoveGeneration(self):
        self.rook_check = [] 
        self.knight_check = []
        self.bishop_check = [] 
        self.pawn_check = []

        if self.team == "white":
            if self.pos + 9 == BlackPawn:
                self.pawn_check.append(self.pos + 9)
            if self.pos + 7 == BlackPawn:
                self.pawn_check.append(self.pos + 7)

        if self.team == "black":
            if self.pos - 9 == WhitePawn:
                self.pawn_check.append(self.pos - 9)
            if self.pos - 7 == WhitePawn:
                self.pawn_check.append(self.pos - 7)

        #Takes the current pos and determines if any threats.
        #Will also allow for checking valid positions incase they have check.
        for i in hor_rows:
            for item in i:
                if item == self.pos:
                    intex1 = hor_rows.index(i)
                    itemtex1 = i.index(item)
                    #intex values
                    reset_intex1 = intex1
                    intex_up1 = 8 - intex1
                    intex_down1 = intex1
                    #itemtex values
                    reset_itemtex1 = itemtex1
                    itemtex_right1 = itemtex1
                    itemtex_left1 = 8 - itemtex1

        #Vertical Up
        lopbol = True
        count = 0
        while count < intex_up1 and lopbol == True:
            intex1 += 1
            try: 
                self.rook_check.append(hor_rows[intex1][itemtex1])
            except:
                break
            for i in pieces:
                if hor_rows[intex1][itemtex1] == i.pos:
                    lopbol = False
                    check_pos = hor_rows[intex1][itemtex1]
                    for piece in pieces:
                        if piece.pos == check_pos:
                            if piece.team == self.team:
                                self.rook_check.remove(check_pos)

            count += 1

        #Vertical Down
        lopbol = True
        count = 0
        intex1 = reset_intex1
        while count < intex_down1 and lopbol == True:
            intex1 -= 1
            try: 
                self.rook_check.append(hor_rows[intex1][itemtex1])
            except:
                break
            for i in pieces:
                if hor_rows[intex1][itemtex1] == i.pos:
                    lopbol = False
            count += 1

        #Horizontal Left
        count = 0
        lopbol = True
        intex1 = reset_intex1
        while count < itemtex_left1 and lopbol == True:
            itemtex1 += 1
            try: 
                self.rook_check.append(hor_rows[intex1][itemtex1])
            except:
                break
            for i in pieces:
                if hor_rows[intex1][itemtex1] == i.pos:
                    lopbol = False
            count += 1

        #Horizontal Right
        count = 0
        lopbol = True
        itemtex1 = reset_itemtex1
        while count < itemtex_right1 and lopbol == True:
            itemtex1 -= 1
            try: 
                self.rook_check.append(hor_rows[intex1][itemtex1])
            except:
                break
            for i in pieces:
                if hor_rows[intex1][itemtex1] == i.pos:
                    lopbol = False
            count += 1

        for i in hor_rows:
            for item in i:
                if item == self.pos:
                    intex = hor_rows.index(i)
                    itemtex = i.index(item)
                    #intex values
                    reset_intex = intex
                    intex_down = intex
                    intex_up = 7 - intex
                    #itemtex values
                    reset_itemtex = itemtex
                    itemtex_right = itemtex
                    intex_down2 = intex_down

        #Diagonal Up-Left
        count = 0
        lopbol = True
        while count < intex_up and lopbol == True:
            itemtex += 1
            intex += 1

            try:
                self.bishop_check.append(hor_rows[intex][itemtex])
            except:
                break
            for i in pieces:
                if hor_rows[intex][itemtex] == i.pos:
                    lopbol = False
            count += 1

        #Diagonal Down-Right 
        count = 0
        lopbol = True
        itemtex = reset_itemtex
        intex  = reset_intex
        while count < intex_down and lopbol == True:
            itemtex -= 1
            intex -= 1

            try:
                self.bishop_check.append(hor_rows[intex][itemtex])
            except:
                break
            for i in pieces:
                if hor_rows[intex][itemtex] == i.pos:
                    lopbol = False
            count += 1

        #Diagonal Up-Right
        count = 0
        lopbol = True
        intex = reset_intex
        itemtex = reset_itemtex
        while count < itemtex_right and lopbol == True:
            itemtex -= 1
            intex += 1

            try:
                self.bishop_check.append(hor_rows[intex][itemtex])
            except:
                break
            for i in pieces:
                if hor_rows[intex][itemtex] == i.pos:
                    lopbol = False
            count += 1

        #Diagonal Down-Left
        count = 0
        lopbol = True
        intex = reset_intex
        itemtex = reset_itemtex
        while count < intex_down2 and lopbol == True:
            itemtex += 1
            intex -= 1

            try:
                self.check.append(hor_rows[intex][itemtex])
            except:
                break

            for i in pieces:
                if hor_rows[intex][itemtex] == i.pos:
                    lopbol = False
            count += 1

        #Knight Checks
        up_left = self.pos + 17
        left_up = self.pos + 10
        left_down = self.pos - 6
        down_left = self.pos - 15

        up_right = self.pos + 15
        right_up = self.pos + 6
        right_down = self.pos - 10
        down_right = self.pos - 17

        self.knight_check.append(up_left)
        self.knight_check.append(left_up)
        self.knight_check.append(left_down)
        self.knight_check.append(down_left)

        self.knight_check.append(up_right)
        self.knight_check.append(right_up)
        self.knight_check.append(right_down)
        self.knight_check.append(down_right)

        if self.pos in outer_left:
            try:
                self.knight_check.remove(up_left)
                self.knight_check.remove(left_up)
                self.knight_check.remove(left_down)
                self.knight_check.remove(down_left)
            except:
                pass

        if self.pos in left:
            try:
                self.knight_check.remove(left_up)
                self.knight_check.remove(left_down)
            except:
                pass    
        
        if self.pos in right:
            try:
                self.knight_check.remove(right.up)
                self.knight_check.remove(right_down)
            except:
                pass

        if self.pos in outer_right:
            try:
                self.knight_check.remove(up_right)
                self.knight_check.remove(right_up)
                self.knight_check.remove(right_down)
                self.knight_check.remove(down_right)
            except:
                pass

        if self.pos in outer2_bot:
            try:
                self.knight_check.remove(down_left)
                self.knight_check.remove(down_right)
                self.knight_check.remove(right_down)
                self.knight_check.remove(left_down)
            except:
                pass

        if self.pos in outer_bot:
            try:
                self.knight_check.remove(down_left)
                self.knight_check.remove(down_right)
            except:
                pass

        if self.pos in outer_top:
            try:
                self.knight_check.remove(up_left)
                self.knight_check.remove(up_right)
            except:
                pass
        
        if self.pos in outer2_top:
            try:
                self.knight_check.remove(up_left)
                self.knight_check.remove(up_right)
                self.knight_check.remove(right_up)
                self.knight_check.remove(left_up)
            except:
                pass

        for i in self.knight_check:
            if i < 0:
                self.knight_check.remove(i)
            if i > 64:
                self.knight_check.remove(i)   

    def clearCheckMoves(self):
        #Again no queen since queen will be determined using rook and bishop moves.
        #Instead including it in checking the piece name for kingCheck.
        self.rook_check = []
        self.knight_check = []
        self.bishop_check = []
        self.pawn_check = []                     

    def moveGeneration(self):
        for i in hor_rows:
            for item in i:
                if item == self.pos:
                    intex1 = hor_rows.index(i)
                    itemtex1 = i.index(item)
                    #intex values
                    reset_intex1 = intex1
                    intex_up1 = (intex1 - intex1) + 1
                    intex_down1 = intex1
                    #itemtex values
                    reset_itemtex1 = itemtex1
                    itemtex_right1 = (itemtex1 - itemtex1) + 1
                    itemtex_left1 = (itemtex1 - itemtex1) + 1

        #Vertical Up
        lopbol = True
        count = 0
        while count < intex_up1 and lopbol == True:
            intex1 += 1
            try: 
                self.moves.append(hor_rows[intex1][itemtex1])
            except:
                break
            for i in pieces:
                if hor_rows[intex1][itemtex1] == i.pos:
                    lopbol = False
            count += 1

        #Vertical Down
        lopbol = True
        count = 0
        intex1 = reset_intex1
        #if loop to check edgecase
        while count < intex_down1 and lopbol == True:
            intex1 -= 1
            try: 
                self.moves.append(hor_rows[intex1][itemtex1])
                break
            except:
                break
            for i in pieces:
                if hor_rows[intex1][itemtex1] == i.pos:
                    lopbol = False
            count += 1

        #Horizontal Left
        count = 0
        lopbol = True
        intex1 = reset_intex1
        while count < itemtex_left1 and lopbol == True:
            itemtex1 += 1
            try: 
                self.moves.append(hor_rows[intex1][itemtex1])
            except:
                break
            for i in pieces:
                if hor_rows[intex1][itemtex1] == i.pos:
                    lopbol = False
            count += 1

        #Horizontal Right
        count = 0
        lopbol = True
        itemtex1 = reset_itemtex1
        while count < itemtex_right1 and lopbol == True:
            itemtex1 -= 1
            try: 
                self.moves.append(hor_rows[intex1][itemtex1])
            except:
                break
            for i in pieces:
                if hor_rows[intex1][itemtex1] == i.pos:
                    lopbol = False
            count += 1

        for i in hor_rows:
            for item in i:
                if item == self.pos:
                    intex = hor_rows.index(i)
                    itemtex = i.index(item)
                    #intex values
                    reset_intex = intex
                    intex_down = intex
                    intex_up = 7 - intex
                    #itemtex values
                    reset_itemtex = itemtex
                    itemtex_right = itemtex
                    intex_down2 = intex_down

        #Diagonal Up-Left
        count = 0
        lopbol = True
        while count < intex_up and lopbol == True:
            itemtex += 1
            intex += 1

            try:
                self.moves.append(hor_rows[intex][itemtex])
                break
            except:
                break
            for i in pieces:
                if hor_rows[intex][itemtex] == i.pos:
                    lopbol = False
            count += 1

        #Diagonal Down-Right 
        count = 0
        lopbol = True
        itemtex = reset_itemtex
        intex  = reset_intex
        while count < intex_down and lopbol == True:
            itemtex -= 1
            intex -= 1

            try:
                self.moves.append(hor_rows[intex][itemtex])
                break
            except:
                break
            for i in pieces:
                if hor_rows[intex][itemtex] == i.pos:
                    lopbol = False
            count += 1

        #Diagonal Up-Right
        count = 0
        lopbol = True
        intex = reset_intex
        itemtex = reset_itemtex
        while count < itemtex_right and lopbol == True:
            itemtex -= 1
            intex += 1

            try:
                self.moves.append(hor_rows[intex][itemtex])
                break
            except:
                break
            for i in pieces:
                if hor_rows[intex][itemtex] == i.pos:
                    lopbol = False
            count += 1

        #Diagonal Down-Left
        count = 0
        lopbol = True
        intex = reset_intex
        itemtex = reset_itemtex
        while count < intex_down2 and lopbol == True:
            itemtex += 1
            intex -= 1

            try:
                self.moves.append(hor_rows[intex][itemtex])
                break
            except:
                break

            for i in pieces:
                if hor_rows[intex][itemtex] == i.pos:
                    lopbol = False
            count += 1

        for i in self.moves:
            for piece in pieces:
                if i == piece.pos:
                    if self.team == piece.team:
                        self.moves.remove(i)

class Queen():
    def __init__(self, team, name, pos):
        self.name = name
        self.pos = pos
        self.team = team
        if self.team == "white":
            self.symbol = "♕"
        elif self.team == "black":
            self.symbol = "♛"
        self.moves = []

    def moveGeneration(self):
        for i in hor_rows:
            for item in i:
                if item == self.pos:
                    intex1 = hor_rows.index(i)
                    itemtex1 = i.index(item)
                    #intex values
                    reset_intex1 = intex1
                    intex_up1 = 8 - intex1
                    intex_down1 = intex1
                    #itemtex values
                    reset_itemtex1 = itemtex1
                    itemtex_right1 = itemtex1
                    itemtex_left1 = 8 - itemtex1

        #Vertical Up
        lopbol = True
        count = 0
        while count < intex_up1 and lopbol == True:
            intex1 += 1
            try: 
                self.moves.append(hor_rows[intex1][itemtex1])
            except:
                break
            for i in pieces:
                if hor_rows[intex1][itemtex1] == i.pos:
                    lopbol = False
            count += 1

        #Vertical Down
        lopbol = True
        count = 0
        intex1 = reset_intex1
        while count < intex_down1 and lopbol == True:
            intex1 -= 1
            try: 
                self.moves.append(hor_rows[intex1][itemtex1])
            except:
                break
            for i in pieces:
                if hor_rows[intex1][itemtex1] == i.pos:
                    lopbol = False
            count += 1

        #Horizontal Left
        count = 0
        lopbol = True
        intex1 = reset_intex1
        while count < itemtex_left1 and lopbol == True:
            itemtex1 += 1
            try: 
                self.moves.append(hor_rows[intex1][itemtex1])
            except:
                break
            for i in pieces:
                if hor_rows[intex1][itemtex1] == i.pos:
                    lopbol = False
            count += 1

        #Horizontal Right
        count = 0
        lopbol = True
        itemtex1 = reset_itemtex1
        while count < itemtex_right1 and lopbol == True:
            itemtex1 -= 1
            try: 
                self.moves.append(hor_rows[intex1][itemtex1])
            except:
                break
            for i in pieces:
                if hor_rows[intex1][itemtex1] == i.pos:
                    lopbol = False
            count += 1

        for i in hor_rows:
            for item in i:
                if item == self.pos:
                    intex = hor_rows.index(i)
                    itemtex = i.index(item)
                    #intex values
                    reset_intex = intex
                    intex_down = intex
                    intex_up = 7 - intex
                    #itemtex values
                    reset_itemtex = itemtex
                    itemtex_right = itemtex
                    intex_down2 = intex_down

        #Diagonal Up-Left
        count = 0
        lopbol = True
        while count < intex_up and lopbol == True:
            itemtex += 1
            intex += 1

            try:
                self.moves.append(hor_rows[intex][itemtex])
            except:
                break
            for i in pieces:
                if hor_rows[intex][itemtex] == i.pos:
                    lopbol = False
            count += 1

        #Diagonal Down-Right 
        count = 0
        lopbol = True
        itemtex = reset_itemtex
        intex  = reset_intex
        while count < intex_down and lopbol == True:
            itemtex -= 1
            intex -= 1

            try:
                self.moves.append(hor_rows[intex][itemtex])
            except:
                break
            for i in pieces:
                if hor_rows[intex][itemtex] == i.pos:
                    lopbol = False
            count += 1

        #Diagonal Up-Right
        count = 0
        lopbol = True
        intex = reset_intex
        itemtex = reset_itemtex
        while count < itemtex_right and lopbol == True:
            itemtex -= 1
            intex += 1

            try:
                self.moves.append(hor_rows[intex][itemtex])
            except:
                break
            for i in pieces:
                if hor_rows[intex][itemtex] == i.pos:
                    lopbol = False
            count += 1

        #Diagonal Down-Left
        count = 0
        lopbol = True
        intex = reset_intex
        itemtex = reset_itemtex
        while count < intex_down2 and lopbol == True:
            itemtex += 1
            intex -= 1

            try:
                self.moves.append(hor_rows[intex][itemtex])
            except:
                break

            for i in pieces:
                if hor_rows[intex][itemtex] == i.pos:
                    lopbol = False
            count += 1

pieces = []
#Starting pos of all pieces.
#Rooks
wrook1 = Rook("white", "wrook1", 15)
pieces.append(wrook1)
# wrook2 = Rook("white", "wrook2", 8)
# pieces.append(wrook2)

brook1 = Rook("black", "brook1", 64)
pieces.append(brook1)
# brook2 = Rook("black", "brook2", 57)
# pieces.append(brook2)

#Knights
# wknight1 = Knight("white", "wnight1", 2)
# pieces.append(wknight1)
# wknight2 = Knight("white", "wnight2", 7)
# pieces.append(wknight2)

# bknight1 = Knight("black", "brook1", 63)
# pieces.append(bknight1)
# bknight2 = Knight("black", "brook2", 58)
# pieces.append(bknight2)

#Bishops
# wbishop1 = Bishop("white", "wbishop1", 3)
# pieces.append(wbishop1)
# wbishop2 = Bishop("white", "wbisop2", 6)
# pieces.append(wbishop2)

# bbishop1 = Bishop("black", "bbishop1", 62)
# pieces.append(bbishop1)
# bbishop2 = Bishop("black", "bbishop2", 59)
# pieces.append(bbishop2)

#Kings
wking = King("white", "wking", 5)
pieces.append(wking)
bking = King("black", "bking", 61)
pieces.append(bking)

#Queens
# wquen = Queen("white", "wquen1", 4)
# pieces.append(wquen)
# bquen = Queen("black", "bquen1", 60)
# pieces.append(bquen)

#Pawns
# wpawn1 = WhitePawn("white", "wpawn1", 9)
# wpawn2 = WhitePawn("white", "wpawn2", 10)
# wpawn3 = WhitePawn("white", "wpawn3", 11)
# wpawn4 = WhitePawn("white", "wpawn4", 12)
# wpawn5 = WhitePawn("white", "wpawn5", 13)
wpawn6 = WhitePawn("white", "wpawn6", 14)
# wpawn7 = WhitePawn("white", "wpawn7", 15)
# wpawn8 = WhitePawn("white", "wpawn8", 16)
# pieces.append(wpawn1)
# pieces.append(wpawn2)
# pieces.append(wpawn3)
# pieces.append(wpawn4)
# pieces.append(wpawn5)
pieces.append(wpawn6)
# pieces.append(wpawn7)
# pieces.append(wpawn8)

# bpawn1 = BlackPawn("black", "bpawn1", 56)
# bpawn2 = BlackPawn("black", "bpawn2", 55)
# bpawn3 = BlackPawn("black", "bpawn3", 54)
# bpawn4 = BlackPawn("black", "bpawn4", 53)
# bpawn5 = BlackPawn("black", "bpawn5", 52)
# bpawn6 = BlackPawn("black", "bpawn6", 51)
# bpawn7 = BlackPawn("black", "bpawn7", 50)
# bpawn8 = BlackPawn("black", "bpawn8", 49)
# pieces.append(bpawn1)
# pieces.append(bpawn2)
# pieces.append(bpawn3)
# pieces.append(bpawn4)
# pieces.append(bpawn5)
# pieces.append(bpawn6)
# pieces.append(bpawn7)
# pieces.append(bpawn8)
    
def makeMove(self, pos=int):
    canExecute = False
    if pos in self.moves:
        canExecute = True
    else:
        canExecute = False

    posTaken = False
    if canExecute == True:
        for i in pieces:
            if i.pos == pos:
                if i.team != self.team:
                    piece = i
                    posTaken = True
                    break
                elif i.team == self.team:
                    canExecute = False
                else:
                    posTaken = False

    if canExecute == True and posTaken == True:
        self.pos = piece.pos
        piece.pos = 65

    if canExecute == True and posTaken == False:
        self.pos = pos    
    
def clearMoves(self):
    self.moves = []

#Converting board into cli display.
def printBoard():
    board = [1 , 2 , 3 , 4 , 5 , 6 , 7 , 8 ,
        9 , 10, 11, 12, 13, 14, 15, 16, 
        17, 18, 19, 20, 21, 22, 23, 24, 
        25, 26, 27, 28, 29, 30, 31, 32, 
        33, 34, 35, 36, 37, 38, 39, 40, 
        41, 42, 43, 44, 45, 46, 47, 48, 
        49, 50, 51, 52, 53, 54, 55, 56, 
        57, 58, 59, 60, 61, 62, 63, 64]
    board_reset = board.copy()

    for piece in pieces:
        for i in board:
            if i == piece.pos:
                itemtex = board.index(i)
                board.remove(i)
                board.insert(itemtex, piece.symbol)

    print(board[0:8])
    print(board[8:16])
    print(board[16:24])
    print(board[24:32])
    print(board[32:40])
    print(board[40:48])
    print(board[48:56])
    print(board[56:64])
    print("\n")

    board = board_reset

def clearAllMoves():
    for piece in pieces:
        piece.moves = []

#Function for making and unmaking moves to check legality. Make/Unmake.
#Main difference between this and "makeMove" is that this function does not remove pieces
#position and instead checks using a "taken" piece's pos.
def legalMakeMove(self, pos):
    canExecute = False
    if pos in self.moves:
        canExecute = True
    else:
        canExecute = False

    posTaken = False
    if canExecute:
        for i in pieces:
            if i.pos == pos:
                if i.team != self.team:
                    piece = i
                    posTaken = True
                    break
                elif i.team == self.team:
                    canExecute = False
                else:
                    posTaken = False

    if canExecute == True and posTaken == True:
        self.pos = piece.pos

    if canExecute == True and posTaken == False:
        self.pos = pos   

#For own team making compromising moves. 
#This does not include enemy causing a check on their turn.
#Also generates all specified piece moves.
def legalMoves():
    if gameTurn == "white":
        for piece in pieces:
            reset = piece.pos
            if piece.team == "white":
                piece.moveGeneration()
                for move in reversed(piece.moves): #reversed list mostly for keeping pawn's double move available
                    legalMakeMove(piece, move)
                    wking.checkMoveGeneration()
                    if kingCheck(wking):
                        print(f"White-King Check! From move {move}!")
                        time.sleep(.5)
                        piece.moves.remove(move)
                    wking.clearCheckMoves()
            piece.pos = reset

    if gameTurn == "black":
        for piece in pieces:
            if piece.team == "black":
                reset = piece.pos
                piece.moveGeneration()
                for move in reversed(piece.moves):
                    legalMakeMove(piece, move)
                    bking.checkMoveGeneration()
                    if kingCheck(bking):
                        print(f"Black-King Check! From move {move}!")
                        time.sleep(.5)
                        piece.moves.remove(move)
                    bking.clearCheckMoves()
                piece.pos = reset
            

def gameTesting():
    global gameTurn
    pnames = []
    active = True
    while active:
        time.sleep(1.5)
        printBoard()
        if gameTurn == "white":
            for piece in pieces:
                if piece.team == "white":
                    pnames.append(piece.name)
        if gameTurn == "black":
            for piece in pieces:
                if piece.team == "black":
                    pnames.append(piece.name)

        legalMoves()

        print(pnames)
        pnames = []

        name_loop = True
        while name_loop:
            piece_selection = input("Which piece would you like to move?\n") 
            for piece in pieces:
                if piece.name == piece_selection:
                    if piece.team == gameTurn and piece.moves != []:
                        piece_call = piece
                        name_loop = False
                    elif not piece.moves:
                        print("There are no legal moves for this piece.")
        
        print(f"Available moves of {piece_selection} are: \n{piece_call.moves}")

        move_loop = True
        while move_loop and name_loop == False:
            piece_move = input("Where should it move?\n")
            for move in piece_call.moves:
                try:
                    if int(piece_move) == move:
                        move_loop = False
                except:
                    print("There was an error with checking the entered piece move.")
        try:
            makeMove(piece_call, int(piece_move))
            clearMoves(piece_call)
        except:
            print("There was an error making the move.")

        clearAllMoves()

        gameTurnComplete()

gameTesting()
