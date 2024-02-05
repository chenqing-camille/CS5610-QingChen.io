from game_controller import GameController
from checkerboard import CheckerBoard

def test_constructor():
    gc = GameController("any")
    TURN = 'black'
    SELECTED = None
    VALID_MOVES = []
    CAPTURED_MOVES = []
    assert gc.turn == TURN and\
            gc.selected == SELECTED and \
            gc.valid_moves == VALID_MOVES and \
            gc.captured_moves == CAPTURED_MOVES

def test_check_game_over():
    gc = GameController("any")
    assert gc.checker_board.count_checkers("red") == 12 and \
            gc.checker_board.move_count < 100 and \
            gc.checker_board.count_checkers("black") == 12 and \
            gc.checker_board.get_piece_moves('black') and \
                not gc.check_game_over()