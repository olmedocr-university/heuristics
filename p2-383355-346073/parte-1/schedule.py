from constraint import *

mon = range(0, 3)
tue = range(4, 7)
wed = range(8, 11)
thu = range(12, 14)

first = [0, 4, 8, 12]

# Mon@1st = 0, ... , Tue@1st = 4, ... , Thu@2nd = 13
subjects = {
    'NSC1': [2, 6, 10, 13],
    'NSC2': [2, 6, 10, 13],
    'HSC1': [0, 1, 2, 4, 5, 6, 8, 9, 10, 12, 13],
    'HSC2': [0, 1, 2, 4, 5, 6, 8, 9, 10, 12, 13],
    'SP1': [0, 1, 2, 4, 5, 6, 8, 9, 10, 12, 13],
    'SP2': [0, 1, 2, 4, 5, 6, 8, 9, 10, 12, 13],
    'MAT1': [0, 4, 8, 12],
    'MAT2': [0, 4, 8, 12],
    'EN1': [0, 1, 2, 4, 5, 6, 8, 9, 10, 12, 13],
    'EN2': [0, 1, 2, 4, 5, 6, 8, 9, 10, 12, 13],
    'PE': [0, 1, 2, 4, 5, 6, 8, 9, 10, 12, 13]
}

# NSC = 0, HSC = 1, ... , PE = 5
teachers = {
    'LUC1': [1],
    'LUC2': [0, 1, 2, 3, 4, 5],
    'AND1': [5],
    'AND2': [0, 1, 2, 3, 4, 5],
    'JUA1': [0, 1, 2, 3, 4, 5],
    'JUA2': [0, 1, 2, 3, 4, 5],
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


def is_not_at_first_hour(a):
    return a not in first


problem = Problem()

for key, value in subjects.items():
    problem.addVariable(key, value)

for key, value in teachers.items():
    problem.addVariable(key, value)

# All subjects must be in different time slots
problem.addConstraint(AllDifferentConstraint(), [*subjects.keys()])

# Human & social science class must be consecutive
problem.addConstraint(is_consecutive, ('HSC1', 'HSC2'))

# MAT-NSC & MAT-EN cannot be taught on the same day
# TODO: rewrite this to include lists instead of manually performing the cartesian product
problem.addConstraint(is_not_on_the_same_day, ('MAT1', 'NSC1'))
problem.addConstraint(is_not_on_the_same_day, ('MAT1', 'NSC2'))
problem.addConstraint(is_not_on_the_same_day, ('MAT2', 'NSC1'))
problem.addConstraint(is_not_on_the_same_day, ('MAT2', 'NSC2'))
problem.addConstraint(is_not_on_the_same_day, ('MAT1', 'EN1'))
problem.addConstraint(is_not_on_the_same_day, ('MAT1', 'EN2'))
problem.addConstraint(is_not_on_the_same_day, ('MAT2', 'EN1'))
problem.addConstraint(is_not_on_the_same_day, ('MAT2', 'EN2'))

# All teachers must lecture different subjects
problem.addConstraint(AllDifferentConstraint(), [*teachers.keys()])

# problem.addConstraint(is_not_at_first_hour, )

print(problem.getSolution())
