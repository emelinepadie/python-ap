import vie.py

def test_complete_with_zeros():
    assert vie.complete_with_zeros([1, 1, 1], 5) == [1, 1, 1, 0, 0] 
    assert vie.complete_with_zeros([1, 1, 1], 3) == [1, 1, 1]
    assert vie.complete_with_zeros([1, 1, 1], 0) == []

def test_open_file():
    assert vie.open_file("tests_game_of_life/test.txt") == [[1, 1, 1], [0, 0, 0], [0, 0, 0]]

def test_init_checkerboard():
    assert vie.init_checkerboard(3, 3, [[1, 1, 1], [0, 0, 0], [0, 0, 0]]) == [[1, 1, 1], [0, 0, 0], [0, 0, 0]]
    assert vie.init_checkerboard(3, 3, [[1, 1, 1], [0, 0, 0]]) == [[1, 1, 1], [0, 0, 0], [0, 0, 0]]
    assert vie.init_checkerboard(3, 3, [[1, 1, 1], [0, 0, 0], [0, 0, 0], [0, 0, 0]]) == [[1, 1, 1], [0, 0, 0], [0, 0, 0]]

def test_mat_living_neighbours():
    assert vie.mat_living_neighbours(3, 3, [[1, 1, 1], [0, 0, 0], [0, 0, 0]]) == [[2, 2, 2], [3, 3, 3], [2, 2, 2]]

def test_evol_game():
    assert vie.evol_game(3, 3, [[1, 1, 1], [0, 0, 0], [0, 0, 0]]) == [[0, 1, 0], [0, 1, 0], [0, 0, 0]]

def test_game_of_life():
    assert vie.game_of_life(3, 3, [[1, 1, 1], [0, 0, 0], [0, 0, 0]]) == [[0, 1, 0], [0, 1, 0], [0, 0, 0]] 
    assert vie.game_of_life(3, 3, [[1, 1, 1], [0, 0, 0], [0, 0, 0]]) == [[0, 1, 0], [0, 1, 0], [0, 0, 0]] 
    assert vie.game_of_life(3, 3, [[1, 1, 1], [0, 0, 0], [0, 0, 0]]) == [[0, 1, 0], [0, 1, 0], [0, 0, 0]] 
    assert vie.game_of_life(3, 3, [[1, 1, 1], [0, 0, 0], [0, 0, 0]]) == [[0, 1, 0], [0, 1, 0], [0, 0, 0]] 
    assert vie.game_of_life(3, 3, [[1, 1, 1], [0, 0, 0], [0, 0, 0]]) == [[0, 1, 0], [0, 1, 0], [0, 0, 0]] 
    assert vie.game_of_life(3, 3, [[1, 1, 1], [0, 0, 0], [0, 0, 0]]) == [[0, 1, 0], [0, 1, 0], [0, 0, 0]] 
    assert vie.game_of_life(3, 3, [[1, 1, 1], [0, 0, 0], [0, 0, 0]]) == [[0, 1, 0], [0, 1, 0], [0, 0, 0]] 
    assert vie.game_of_life(3, 3, [[1, 1, 1], [0, 0, 0], [0, 0, 0]]) == [[0, 1, 0], [0, 1, 0], [0, 0, 0]]

def test_main():
    assert vie.main(3, 3, 3, 3) == [[0, 1, 0], [0, 1, 0], [0, 0, 0]] 
    assert vie.main(3, 3, 3, 3) == [[0, 1, 0], [0, 1, 0], [0, 0, 0]] 
    assert vie.main(3, 3, 3, 3) == [[0, 1, 0], [0, 1, 0], [0, 0, 0]] 
    assert vie.main(3, 3, 3, 3) == [[0, 1, 0], [0, 1, 0], [0, 0, 0]] 
    assert vie.main(3, 3, 3, 3) == [[0, 1, 0], [0, 1, 0], [0, 0, 0]] 
    assert vie.main(3, 3, 3, 3) == [[0, 1, 0], [0, 1, 0], [0, 0, 0]] 
    assert vie.main(3, 3, 3, 3) == [[0, 1, 0], [0, 1, 0], [0, 0, 0]] 
    assert vie.main(3, 3, 3, 3) == [[0, 1, 0], [0, 1, 0], [0, 0, 0]] 
    assert vie.main(3, 3, 3, 3) == [[0, 1, 0], [0, 1, 0], [0, 0, 0]] 
    assert vie.main(3, 3, 3, 3) == [[0, 1, 0], [0, 1, 0], [0, 0, 0]] 
    assert vie.main(3, 3, 3, 3) == [[0, 1, 0], [0, 1, 0], [0, 0, 0]] 
    assert vie.main(3, 3, 3, 3) == [[0, 1, 0], [0, 1, 0], [0, 0, 0]]




