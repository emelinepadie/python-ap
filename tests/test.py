import sequence.py 

## test 
def tests_align_1():
    assert sequence.align_1('', '', -2, 1, -1) == ([0], [''])
    assert sequence.align_1('A', 'A', -2, 1, -1) == ([[0, -2], [-2, 1]], [['', 'left'], ['up', 'diag']])
