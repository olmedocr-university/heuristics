from constraint import *

mon = range(0, 3)
tue = range(4, 7)
wed = range(8, 11)
thu = range(12, 14)

NSC = ['NSC1', 'NSC2']
HSC = ['HSC1', 'HSC2']
SP = ['SP1', 'SP2']
MAT = ['MAT1', 'MAT2']
EN = ['EN1', 'EN2']
PE = ['PE']

var_dict = {
    'NSC': [2, 6, 10, 13],
    'HSC': [0, 1, 2, 4, 5, 6, 8, 9, 10, 12, 13],
    'SP': [0, 1, 2, 4, 5, 6, 8, 9, 10, 12, 13],
    'MAT': [0, 4, 8, 12],
    'EN': [0, 1, 2, 4, 5, 6, 8, 9, 10, 12, 13],
    'PE': [0, 1, 2, 4, 5, 6, 8, 9, 10, 12, 13]
}


def is_consecutive(a, b):
    return a + 1 == b or a == b + 1


def is_not_on_the_same_day(a, b):
    if a in mon:
        return b not in mon
    elif a in tue:
        return b not in tue
    elif a in wed:
        return b not in wed
    elif a in thu:
        return b not in thu
    else:
        return False


problem = Problem()

problem.addVariable('NSC1', [2, 6, 10, 13])
problem.addVariable('NSC2', [2, 6, 10, 13])
problem.addVariable('HSC1', [0, 1, 2, 4, 5, 6, 8, 9, 10, 12, 13])
problem.addVariable('HSC2', [0, 1, 2, 4, 5, 6, 8, 9, 10, 12, 13])
problem.addVariable('SP1', [0, 1, 2, 4, 5, 6, 8, 9, 10, 12, 13])
problem.addVariable('SP2', [0, 1, 2, 4, 5, 6, 8, 9, 10, 12, 13])
problem.addVariable('MAT1', [0, 4, 8, 12])
problem.addVariable('MAT2', [0, 4, 8, 12])
problem.addVariable('EN1', [0, 1, 2, 4, 5, 6, 8, 9, 10, 12, 13])
problem.addVariable('EN2', [0, 1, 2, 4, 5, 6, 8, 9, 10, 12, 13])
problem.addVariable('PE', [0, 1, 2, 4, 5, 6, 8, 9, 10, 12, 13])

# All subjects must be in different time slots
problem.addConstraint(AllDifferentConstraint(),
                      ['NSC1', 'NSC2', 'HSC1', 'HSC2', 'SP1', 'SP2', 'MAT1', 'MAT2', 'EN1', 'EN2', 'PE'])

# Natural science class must be consecutive
problem.addConstraint(is_consecutive, ('NSC1', 'NSC2'))

# MAT-NSC & MAT-SP cannot be taught in the same day
problem.addConstraint(is_not_on_the_same_day, ('MAT1', 'NSC1'))
problem.addConstraint(is_not_on_the_same_day, ('MAT1', 'NSC2'))
problem.addConstraint(is_not_on_the_same_day, ('MAT2', 'NSC1'))
problem.addConstraint(is_not_on_the_same_day, ('MAT2', 'NSC2'))
problem.addConstraint(is_not_on_the_same_day, ('MAT1', 'SP1'))
problem.addConstraint(is_not_on_the_same_day, ('MAT1', 'SP2'))
problem.addConstraint(is_not_on_the_same_day, ('MAT2', 'SP1'))
problem.addConstraint(is_not_on_the_same_day, ('MAT2', 'SP2'))

print(problem.getSolutions())


