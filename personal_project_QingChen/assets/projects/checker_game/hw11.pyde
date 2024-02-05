from game_controller import GameController

# Initialize the GameController object

def setup():
    '''
    For your reference, wordsFont is from Minesweeper game of Professor
    '''
    global countdown
    countdown = 0
    global delay_or_not
    delay_or_not = False
    global game_controller
    size(800, 800)
    wordsFont = createFont("BadaboomBB_Reg.otf", 150)
    game_controller = GameController(wordsFont)
    game_controller.setup()

def draw():
    global countdown
    game_controller.draw()
    if countdown == 0:
        delay_or_not = True
        game_controller.AI_move()
    else:
        delay_or_not = False
        countdown -= 1

def initiate_delay(): 
    global countdown
    countdown = 50

def mousePressed():
    game_controller.mousePressed()

def mouseDragged():
    game_controller.mouseDragged()
    
def mouseReleased():
    global delay_or_not
    game_controller.mouseReleased()
    initiate_delay()

