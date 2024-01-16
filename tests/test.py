import sequence.py 

## test 
def tests_needleman():
    assert sequence.needleman_wunsch([''], [''] , -2, -1, 1) == [[0]]
    assert sequence.needleman_wunsch(['A'], ['A'], -2, -1, 1) == [[0, -2], [-2, 1]]
    assert sequence.needleman_wunsch(["A","G","C"], ['T', 'T', 'T'],-2, -1, 1) == [[0, -2, -4, -6], [-2, -1, -3, -5], [-4, -3, -2, -4], [-6, -5, -4, -3]]
    assert sequence.needleman_wunsch(["A","G","C"], ["A","G","C"], -2, -1, 1) == [[0, -2, -4, -6], [-2, 1, -1, -3], [-4, -1, 2, 0], [-6, -3, 0, 3]]

def tests_traceback():
    assert sequence.traceback(['A', 'A', 'C', 'T', 'G', 'A'], ['G', 'A', 'C', 'G', 'A'], mat =[[0, -2, -4, -6, -8, -10], [-2, -1, -1, -3, -5, -7], [-4, -3, 0, -2, -4, -4], [-6, -5, -2, 1, -1, -3], [-8, -7, -4, -1, 0, -2], [-10, -7, -6, -3, 0, -1], [-12, -9, -6, -5, -2, 1]], gap_penalty=-2, mismatch_penalty=-1, match_score=1) == ('AACTGA', 'GAC-GA', 1)
    assert sequence.traceback([''], [''], [[0]], -2, -1, 1) == ('', '', 0)   
    assert sequence.traceback(['A'], ['A'], [[0, -2], [-2, 1]], -2, -1, 1) == ('A', 'A', 1)
    assert sequence.traceback(['A', 'G', 'C'], ['T', 'T', 'T'], [[0, -2, -4, -6], [-2, -1, -3, -5], [-4, -3, -2, -4], [-6, -5, -4, -3]], -2, -1, 1) == ('AGC', 'TTT', -3)