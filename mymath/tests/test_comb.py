import pytest
import mymath

def test_comb_non_integers():
    with pytest.raises(TypeError):
        mymath.comb(4, 2.5)
    with pytest.raises(TypeError):
        mymath.comb(4.5, 2)
    with pytest.raises(TypeError):
        mymath.comb("5", 2)

def test_comb_negative():
    with pytest.raises(ValueError):
        mymath.comb(-1, 1)
    with pytest.raises(ValueError):
        mymath.comb(1, -1)

def test_comb_k_greater_than_n():
    assert mymath.comb(0, 1) == 0
    assert mymath.comb(1, 2) == 0

def test_comb():
    assert mymath.comb(0, 0) == 1
    assert mymath.comb(1, 0) == 1
    assert mymath.comb(1, 1) == 1
    assert mymath.comb(2, 1) == 2
    assert mymath.comb(3, 1) == 3
    assert mymath.comb(3, 2) == 3
    assert mymath.comb(4, 2) == 6
    assert mymath.comb(4, 4) == 1
