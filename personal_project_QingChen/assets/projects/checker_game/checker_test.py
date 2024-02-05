from checker import Checker


def test_constructor():
    COLOR = "black"
    X = 1
    Y = 2
    checker = Checker(COLOR, X, Y)
    assert checker.color == COLOR and checker.x == 150 and checker.y == 250


def test_set_position():
    checker1 = Checker(("black"), 1, 2)
    checker1.set_position(1, 2) 
    assert checker1.x == 150 and checker1.y == 250
    checker1.set_position(0, 0) 
    assert checker1.x == 50 and checker1.y == 50


def test_move():
    checker2 = Checker(("black"), 1, 2)
    checker2.move(0, 1)
    assert checker2.x == 50 and checker2.y == 150
    checker2.move(1, 0)
    assert checker2.x == 150 and checker2.y == 50


def test_pick():
    checker3 = Checker(("black"), 1, 2)
    checker3.pick()
    assert checker3.picked == True
    checker3.unpick()
    assert checker3.picked == False


def test_make_king():
    checker4 = Checker(("black"), 1, 2)
    assert checker4.king == False
    checker4.make_king()
    assert checker4.king == True
