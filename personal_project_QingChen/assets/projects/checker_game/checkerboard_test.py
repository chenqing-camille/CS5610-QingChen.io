from checkerboard import CheckerBoard
from checker import Checker

def test_constructor():
    squares = 4
    cb = CheckerBoard(squares)
    assert cb.NUM_SQUARES == 4 and cb.black_kings == cb.red_kings == 0
    squares = 8
    cb = CheckerBoard(squares)
    assert cb.NUM_SQUARES == 8 and cb.black_kings == cb.red_kings == 0


def test_create_board():
    squares = 8
    cb = CheckerBoard(squares)
    cb.create_board()
    assert cb.board[0][1].color == "red" and cb.board[0][1].x == 50 and cb.board[0][1].y == 150
    assert cb.board[0][7].color == "black" and cb.board[0][7].x == 50 and cb.board[0][7].y == 750

def test_get_checker():
    cb = CheckerBoard(8)
    checker = cb.get_checker(0, 1)
    assert checker.color == "red" and checker.x == 50 and checker.y == 150
    checker = cb.get_checker(0, 7)
    assert checker.color == "black" and checker.x == 50 and checker.y == 750

def test_move():
    cb = CheckerBoard(8)
    cb.create_board()
    piece = Checker("black", 0, 7)
    cb.move(piece, 1, 6)
    assert piece.x == 150 and piece.y == 650 and piece.king == False
    cb.move(piece, 1, 0)
    assert piece.x == 150 and piece.y == 50 and piece.king == True

def test_is_valid_square():
    cb = CheckerBoard(8)
    assert cb.is_valid_square(0, 0)
    assert cb.is_valid_square(3, 4)
    assert not cb.is_valid_square(8, 8)
    assert not cb.is_valid_square(9, 0)

def test_get_valid_moves():
    cb = CheckerBoard(8)
    piece = Checker("black", 0, 7)
    assert piece.king == False and cb.get_valid_moves(piece) == []
    piece = Checker("black", 1, 4)
    assert piece.king == False and cb.get_valid_moves(piece) == [(0, 3), (2, 3)]

def test_get_captured_moves():
    cb = CheckerBoard(8)
    piece_jump = Checker("black", 0, 5)
    piece_captured = Checker("red", 1, 4)
    cb.board[2][3] = 0
    cb.board[0][5] = piece_jump
    cb.board[1][4] = piece_captured
    assert cb.is_valid_square(2, 3) == True and \
            cb.is_valid_square(1, 4) == True and \
            piece_captured.color != piece_jump.color and \
            cb.board[2][3] == 0 and \
            cb.get_captured_moves(piece_jump) == [((2, 3), (1, 4))]
        
def test_remove_checker():
    cb = CheckerBoard(8)
    cb.black_left = 12
    piece = Checker("black", 0, 5)
    cb.board[0][5] = piece
    assert cb.black_left == 12
    cb.remove_checker(0, 5)
    assert cb.black_left == 11 and piece != 0

def test_get_all_checkers():
    cb = CheckerBoard(8)
    assert len(cb.get_all_checkers('red')) == 12
    assert len(cb.get_all_checkers('black')) == 12

def test_count_checkers():
    cb = CheckerBoard(8)
    assert cb.count_checkers('red') == 12

def test_get_piece_moves():
    cb = CheckerBoard(8)
    assert len(cb.get_piece_moves('red')) == 4 and \
            len(cb.get_piece_moves('black')) == 4

