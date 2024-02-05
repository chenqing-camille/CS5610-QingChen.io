# Import classes
from checker import Checker
from checkerboard import CheckerBoard
import time

# GameController class
class GameController:
    # Initialize GameController
    def __init__(self, wordsFont):
        self.selected = None
        self.turn = 'black'
        self.valid_moves = []
        self.captured_moves = []
        NUM_SQUARES = 8
        self.checker_board = CheckerBoard(NUM_SQUARES)
        self.turn_complete = False
        self.game_over = False
        self.wordsFont = wordsFont

    # Set up the game
    def setup(self):
        global crown_img
        crown_img = loadImage("crown.png")

    # Draw the game
    def draw(self):
        if not self.game_over:
            self.checker_board.draw()
            for row in range(self.checker_board.NUM_SQUARES):
                for col in range(self.checker_board.NUM_SQUARES):
                        checker = self.checker_board.board[row][col]
                        if checker != 0:
                            checker.draw(crown_img)
            if mouseX <= 800 and mouseY <= 800:
                # if mouse is over the piece, then draw a circular highlighter
                self.mouse_over_piece()
            # if there is any piece can jump over another, then draw the skipped position
            if self.captured_moves:
                self.checker_board.draw_captured_moves(self.captured_moves)
            # captured moves first, if no captured move, get valid moves:
            # show available new position for a specific piece with green square
            elif self.valid_moves:
                self.checker_board.draw_valid_moves(self.valid_moves)

    def mouse_over_piece(self):
        # when the mouse is over the piece without clicking...
        checker = self.checker_board.get_checker_from_mouse()
        if checker!= 0 and (self.checker_board.get_captured_moves(checker) or \
              self.checker_board.get_valid_moves(checker)) and checker.color == 'black':
            checker.is_mouse_over()
        elif checker != 0 and not self.checker_board.get_valid_moves(checker):
            checker.over = False

    # Handle mouse press event
    def mousePressed(self):
        # get the checker by mouse position
        row,col = mouseX//100, mouseY//100
        checker = self.checker_board.get_checker(row, col)
        # if checker is 0 on the board, means no checker at (row, col), then return
        # also, if its opponent's turn, we cannot move, return.
        if checker == 0 or checker.color != self.turn:
            return
        # when we get a black checker as we want, we make the checker selected and picked
        if checker != 0 and checker.color == self.turn :
            checker.pick()
            self.dragging = False
            self.selected = checker
            # when we pressed the checker, show where it could be.
            self.valid_moves = self.checker_board.get_valid_moves(self.selected)
            self.captured_moves = self.checker_board.get_captured_moves(self.selected)
    
    def mouseDragged(self):
        if self.selected and not self.dragging:
            # check if the mouse has moved by a certain amount before starting to drag
            dx = abs(mouseX//100 - self.selected.x//100)
            dy = abs(mouseY//100 - self.selected.y//100)
            # from the distance, we could know the piece is dragged to no matter how far it is.
            if dx > 0 or dy > 0:
                self.dragging = True  # set dragging to True
                self.selected.pick()  # pick up the checker again

    # Handle mouse release event
    def mouseReleased(self):
        self.update()

    def update(self):
        if(self.selected and self.dragging):
            new_x, new_y = mouseX//100, mouseY//100
        # Check if the move is in captured moves
            if self.captured_moves:
                for move in self.captured_moves:
                    if (new_x, new_y) == move[0]:
                        jump, over = move[0], move[1]
                        self.checker_board.move(self.selected, jump[0], jump[1])
                        self.checker_board.remove_checker(over[0], over[1])
                        # Check if there are any more captures
                        new_piece = self.checker_board.get_checker(new_x,new_y)
                        captures = self.checker_board.get_captured_moves(new_piece)
                        if captures:
                            self.turn_complete = False
                            self.captured_moves = captures
                        else:
                            self.turn_complete = True
                            self.selected.unpick()
                            self.selected = None
                            self.turn = "red"
                            self.game_over = self.check_game_over()
                            self.valid_moves = []
                            self.captured_moves = []

            # check if is in valid moves        
            elif (new_x, new_y) in self.valid_moves:
                self.checker_board.move(self.selected, new_x, new_y)
                self.turn = "red"
                self.game_over = self.check_game_over()
                self.selected.unpick()
                self.selected = None
                self.valid_moves = []
                self.captured_moves = []       
                self.dragging = False  
                self.turn_complete = True 
            else:
                self.game_over = self.check_game_over()
                print("you can not move here")
                return
        elif not self.selected:
            pass
        elif not self.dragging:
            self.selected.unpick()
            self.selected = None
            self.valid_moves = []
            self.captured_moves = []       
            self.dragging = False
            self.game_over = self.check_game_over()

    def AI_move(self):
        if self.turn_complete and self.turn == "red":
            self.checker_board.ai_move()
            self.game_over = self.check_game_over()
            self.turn = "red" if self.turn == "black" else "black"

    def check_game_over(self):
        # Check if one player has no more pieces on the board
        red_count = self.checker_board.count_checkers("red")
        black_count = self.checker_board.count_checkers("black")

        # in case no leagal moves before game ends
        other_player = "Red" if self.turn == "Black" else "Black"
        current_piece_count = self.checker_board.count_checkers(other_player)
        legal_moves = self.checker_board.get_piece_moves(other_player)

        if self.checker_board.move_count >= 100:
            self.over_50_moves()
            return True
        elif red_count == 0:
            self.end_game("Black")
            self.user_scores()
            return True
        elif black_count == 0:
            self.end_game("Red")
            # print("Red wins!")  # Black has no more pieces on the board.
            return True
         # Check if the current player has no legal moves
        elif current_piece_count > 0 and legal_moves is None:
            self.end_game(self.turn)
            return True
        return False

    # both human and computer has moved 50 times, game over. display "DRAW"
    def over_50_moves(self):
        message = "Draw!" # Red has no more pieces on the board.
        offset = 3
        textAlign(CENTER)
        textFont(self.wordsFont)
        fill(0)
        text(message, 400+offset, 400+offset)
        fill(255)
        text(message, 400, 400)

    # display the end game text and show the winner
    def end_game(self, winner):
        message = winner + " Wins!"  # Red has no more pieces on the board.
        offset = 3
        textAlign(CENTER)
        textFont(self.wordsFont)
        fill(0)
        text(message, 400+offset, 400+offset)
        fill(255)
        text(message, 400, 400)
        # if winner == "black":
        #     self.user_scores()

    # if black wins, then record the user name and win times in the file scores.txt
    def user_scores(self):
        answer = self.input('enter your name')
        dict_user_score = {}
        if answer:
            print('hi ' + answer)
        elif answer == '':
            print('[empty string]')
        else:
            print(answer) # Canceled dialog will print None

        with open("scores.txt") as f:
            for line in f:
                if answer in line:
                    dict_user_score[answer] += 1
                else:
                    dict_user_score[answer] = 1
    
        # record user's win times from highest to lowest
        with open("scores.txt", "a") as f:
            sorted_dict = dict(sorted(dict_user_score.items(),
                                key=lambda x: x[1],
                                reverse=True))
            for user, score in sorted_dict.items():
                # collect user information: name and win times
                user_info = user + "    " + str(score) + "\n"
                f.write(user_info)
        # f.close()

    def input(self, message=''):
        from javax.swing import JOptionPane
        return JOptionPane.showInputDialog(frame, message)
