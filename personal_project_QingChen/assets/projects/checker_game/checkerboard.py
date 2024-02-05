from checker import Checker
import random


# CheckerBoard class
class CheckerBoard:
    # Initialize checker board
    def __init__(self, squares):
        self.NUM_SQUARES = squares
        self.red_left = self.black_left = 12
        self.red_kings = self.black_kings = 0
        self.board = []
        self.create_board()
        self.move_count = 0
        self.black_move = 0

    # Draw checker board
    def draw(self):
        # size for each square on the board
        CELL_SIZE = 100
        BOARD_SIZE = 800
        LIGHT_CELL = color(222, 184, 135)  # burlywood
        DARK_CELL = color(160, 82, 45)  # BROWN
        noStroke()
        square(0, 0, BOARD_SIZE)

        # draw all checkers on the board.
        for i in range(0, BOARD_SIZE, CELL_SIZE * 2):
            for j in range(0, BOARD_SIZE, CELL_SIZE * 2):
                fill(LIGHT_CELL)
                square(i, j, CELL_SIZE)
                square(i + CELL_SIZE, j + CELL_SIZE, CELL_SIZE)
                fill(DARK_CELL)
                square(i, j + CELL_SIZE, CELL_SIZE)
                square(i + CELL_SIZE, j, CELL_SIZE)

    def create_board(self):
        '''
            Function -- create the board:
                According to the squares of different row and col on the board,
                append checkers and collect them in a double list, which make
                the checker is easy to find.
                If no checker in a cell, set its value as 0
        '''
        for row in range(self.NUM_SQUARES):
            self.board.append([])
            for col in range(self.NUM_SQUARES):
                if col % 2 != row % 2:
                    if col < 3:
                        self.board[row].append(Checker("red",row,col))
                    elif col > 4:
                        self.board[row].append(Checker("black",row, col))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)  

    # get the piece of given row and column
    def get_checker(self, row, col):
        return self.board[row][col]                    

    def move(self, piece, row, col):
        '''
            move the piece to the position (row,col)
            Parameters:
              the piece that needs to be moved
              the row and column that want to be moved to

            If the checker arrives at col == 0 or col == 7,
            the checcker is a king, then load the image.
        '''
        self.board[piece.x//100][piece.y//100], self.board[row][col] = \
            self.board[row][col], self.board[piece.x//100][piece.y//100]
        piece.move(row, col)
        self.move_count += 1
        print("move count : ", self.move_count)
        # for each move, the count increments -- overall 100 then draw.
        if col == 0 or col == self.NUM_SQUARES - 1:
            piece.make_king()

    def is_valid_square(self,row, col):
        # Check if row and col are within bounds of the checkerboard
        if row < 0 or row >= self.NUM_SQUARES or col < 0 or col >= self.NUM_SQUARES:
            return False
        # Square is valid
        return True

    def get_valid_moves(self, checker):
        '''
            Parameter: checker
            use this function to calculate whether a piece is avaible for moving.
        '''
        moves = []
        captures = []
        row, col = checker.x//100, checker.y//100
        color = checker.color
        opponent_color = "black" if color == "red" else "red"

        # Step1 according to it's color, decide its directions
        if checker.king:
            directions = [-1, 1]
        elif color == "red":
            directions = [1]
        else:
            directions = [-1]

        for direction in directions:
            for d in [-1, 1]:
                new_row = row + d
                new_col = col + direction
                jump_row = row + 2*d
                jump_col = col + 2*direction

                # Check if new position is on the board
                if not self.is_valid_square(new_row, new_col):
                    continue
                # Check for capturing moves
                if  self.is_valid_square(jump_row, jump_col) and \
                    self.board[jump_row][jump_col] == 0 and \
                    self.board[new_row][new_col] != 0 and \
                    self.board[new_row][new_col].color == opponent_color:
                    # # Check if a jump is mandatory
                    # if captures and captures[0][0] != (jump_row, jump_col):
                    #     continue
                        captures.append(((jump_row, jump_col), (new_row, new_col)))
                # Check for non-capturing moves
                elif self.board[new_row][new_col] == 0:
                    # Check if a jump is mandatory
                    if captures:
                        continue
                    moves.append((new_row, new_col))

        if captures:
            return captures
        else:
            return moves

    # return a list of captured moves
    def get_captured_moves(self, checker):
        captures = []
        row, col = checker.x//100, checker.y//100
        color = checker.color
        opponent_color = "black" if color == "red" else "red"

        if checker.king:
            directions = [-1, 1]
        elif color == "red":
            directions = [1]
        else:
            directions = [-1]

        for direction in directions:
            for d in [-1, 1]:
                new_row = row + d
                new_col = col + direction
                jump_row = row + 2*d
                jump_col = col + 2*direction

                # Check if new position is on the board
                if not self.is_valid_square(new_row, new_col):
                    continue
                # Check if jump position is on the board
                if not self.is_valid_square(jump_row, jump_col):
                    continue
                # Check for capturing moves
                if self.board[jump_row][jump_col] == 0:
                    skipped = self.board[new_row][new_col]
                    if(skipped != 0 and skipped.color == opponent_color):
                        captures.append(((jump_row, jump_col), (new_row, new_col)))
        return captures

    # get a checker by mouse position
    def get_checker_from_mouse(self):
        row, col = mouseX // 100, mouseY // 100
        return self.board[row][col]

    def draw_valid_moves(self,valid_moves):
        for move in valid_moves:
            x, y = move[0] * 100, move[1] * 100
            fill(0, 255, 0, 127)  # Set fill color to green with alpha of 127
            rect(x, y, 100, 100)  # Draw a green rectangle over the valid move square

    def draw_captured_moves(self,captured_moves):
        for move in captured_moves:
            x, y = move[0][0] * 100, move[0][1] * 100
            fill(0, 255, 0, 127)  # Set fill color to green with alpha of 127
            rect(x, y, 100, 100)  # Draw a green rectangle over the valid move square        

    # if a checker is captured, remove it from the board
    def remove_checker(self,row, col):
        piece = self.board[row][col]
        if (piece.color == "black" and piece != 0):
            self.black_left -= 1
        elif (piece.color == "red" and piece != 0):
            self.red_left -= 1 
        self.board[row][col] = 0

    # return list of pieces on the board given the color
    def get_all_checkers(self,color):
        pieces = []
        for row in range(self.NUM_SQUARES):
            for col in range(self.NUM_SQUARES):
                piece = self.board[row][col]
                if piece != 0 and piece.color == color:
                    pieces.append(piece)
        return pieces

    # the fuction for computer to move
    def ai_move(self):
        pieces = self.get_all_checkers("red")
        valid_moves = []
        captured_moves = []

        for piece in pieces:
            piece_captured_moves = self.get_captured_moves(piece)
            piece_valid_moves = self.get_valid_moves(piece)
            if piece_captured_moves:
                captured_moves.extend([(piece, move) for move in piece_captured_moves])
            elif piece_valid_moves:
                valid_moves.extend([(piece, move) for move in piece_valid_moves])
        if captured_moves:
            # self.initiate_delay()
        # Select a random move from the available moves
            piece, move = random.choice(captured_moves)
            # If the move is a capture, perform it
            jump, over = move
            self.move(piece, jump[0], jump[1])
            self.remove_checker(over[0], over[1])
            # Check if there are any more captures
            captures = self.get_captured_moves(piece)
            while captures:
                # If there are more captures, perform them
                jump, over = random.choice(captures)
                self.move(piece, jump[0], jump[1])
                self.remove_checker(over[0], over[1])
                captures = self.get_captured_moves(piece)
        elif valid_moves:
            # self.initiate_delay()
            piece, move = random.choice(valid_moves)  
            self.move(piece, move[0], move[1])  
        else:
            # If no moves are available, skip the turn
            print("you can not move anymore, the BLACK WINS")

    # count the number of checker given the color to know winner
    def count_checkers(self,color):
        if color == "red":
            return self.red_left
        else:
            return self.black_left    

    # function used to know all pieces of the same color
    # if the list == None then game over 
    def get_piece_moves(self, color):
        pieces = self.get_all_checkers(color)
        valid_moves = []
        for piece in pieces:
            piece_valid_moves = self.get_valid_moves(piece)
            if piece_valid_moves:
                valid_moves.append(piece_valid_moves)
        return valid_moves        
