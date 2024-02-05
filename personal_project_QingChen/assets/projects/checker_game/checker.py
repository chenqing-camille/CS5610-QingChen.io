# Checker class
class Checker:
    # Initialize checker with color, x and y positions
    # x and y presents board[x][y] initially.
    def __init__(self, color, x, y):
        self.color = color
        self.set_position(x, y)
        self.king = False
        self.picked = False
        self.over = False

    # set position of checker in Processing
    def set_position(self, x, y):
        self.x = x * 100 + 50
        self.y = y * 100 + 50

    # get board position of checker
    def get_board_position(self, x, y):
        return x // 100, y // 100

    # check if mouse is over the checker
    # if true, 
    def is_mouse_over(self):
        distance = dist(mouseX, mouseY, self.x, self.y)
        if  distance < 50:
            # print("I wanna know the true.", dist(mouseX, mouseY, self.x, self.y))
            self.over =  True
        elif distance >= 50:
            # print("I wanna know the false.", dist(mouseX, mouseY, self.x, self.y))
            self.over =  False

    # Draw checker, including cown image if it's a king
    def draw(self, crown_img):
        '''
        The logic of draw a piece on the board.
            if the piece is picked:
                then move it to the new position(mouseX, mouseY)
            if the mouse is over the piece and the piece is available for moving:
                then set a circular highlighter
            else: Not being dragged to a new position, back to the original one.   
        '''
        if self.picked:
            self.draw_checker_with_borders(mouseX, mouseY, 2)
            if self.king:
                image(crown_img, mouseX - 20, mouseY - 20, 40, 40)
        elif self.over:
            self.draw_checker_with_borders(self.x, self.y, 5)
            if self.king:
                image(crown_img, self.x - 20, self.y - 20, 40, 40)
        else:
            self.draw_checker_with_borders(self.x, self.y, 2)
            if self.king:
                image(crown_img, self.x - 20, self.y - 20, 40, 40)

    # Draw checker with white borders
    def draw_checker_with_borders(self, x, y, size):
        '''
            set the boarder as a variable for different cases.
            when the mouse is over the piece, border is bigger 5
            Normal cases are 2
        '''
        circular_border = size
        strokeWeight(circular_border)
        stroke(255)  # White border
        if self.color == 'black':
            fill(0)
        else:
            fill(210, 40, 48)
        strokeWeight(circular_border)
        stroke(255)  # White border
        ellipse(x, y, 95, 95)

        strokeWeight(2)
        stroke(255)  # White inner border
        ellipse(x, y, 75, 75)

    # move the piece by changing its position.
    def move(self, new_row, new_col):
        '''
            Parameters:
                new_row:the designated row to be moved
                new_col:the designated column to be moved
        '''
        self.set_position(new_row,new_col)

    # to know if one piece is picked
    def pick(self):
        self.picked = True

    # unpick the piece when the mouse released
    def unpick(self):
        self.picked = False       

    # to make the piece king
    def make_king(self):
        self.king = True
