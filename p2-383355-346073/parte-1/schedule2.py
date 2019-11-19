import constraint

mon = range(0, 3)
tue = range(4, 7)
wed = range(8, 11)
thu = range(12, 14)

first = [0, 4, 8, 12]

NSC = 0
HSC = 1
SP = 2
MAT = 3
EN = 4
PE = 5

# Mon@1st = 0, Mon@2nd = 1, Mon@3rd = 2, Tue@1st = 4, ... , Thu@2nd = 13
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
    'LUC1': [0, 1, 2, 3, 4, 5],
    'LUC2': [0, 1, 2, 3, 4, 5],
    'AND1': [0, 1, 2, 3, 4, 5],
    'AND2': [0, 1, 2, 3, 4, 5],
    'JUA1': [0, 1, 2, 3, 4, 5],
    'JUA2': [0, 1, 2, 3, 4, 5],
}


def is_consecutive(a, b):
    return a + 1 == b or a == b + 1


def is_not_on_the_same_day(a,b,c,d,e,f):
    days=[mon,tue,wed,thu]
    for i in [a,b]:
        for j in days:
            if i in j:
                for k in [c,d,e,f]:
                    if k in j:
                        return False
    return True


def lucia_teaches_hsc(a,b,c,d):
    loop1 = False;
    for i in [c,d]:
        loop1 = loop1 or i==PE
    loop2 = False
    for i in [a,b]:
        loop2 = loop2 or i==HSC
    return (loop1 and loop2) or (not (loop1 and loop2))


def juan_can_teach(a,b,c,d,e,f):
    for i in [a,b]:
        if i == NSC or i == HSC:
            for k in [c,d,e,f]:
                if (k in mon or k in thu) and k in first:
                    return False
    return True


def print_solution(solution):
    # TODO: write the method to beauty print the results
    print("Number of solutions found: {}\n".format(len(solution)))
#   .getSolutions() returns a dictionary
#   for s in solutions:
#       print("NSC = {},{}; HSC = {},{}; SP = {},{}; MAT = {},{}; EN = {},{}; PE = {}; LUCIA = {},{}; ANDREA = {},{}; JUAN = {},{};"
#       .format(s['NSC1'], s['NSC2'], s['HSC1'], s['HSC2'], s['SP1'], s['SP2'], s['MAT1'], s['MAT2'], s['EN1'], s['EN2'], s['PE'], s['LUC1'], s['LUC2'], s['AND1'], s['AND2'], s['JUA1'], s['JUA2']))


problem = constraint.Problem()

for key, value in subjects.items():
    problem.addVariable(key, value)

for key, value in teachers.items():
    problem.addVariable(key, value)

# All subjects must be in different time slots
problem.addConstraint(constraint.AllDifferentConstraint(), [*subjects.keys()])

# Human & social science class must be consecutive
problem.addConstraint(is_consecutive, ('HSC1', 'HSC2'))

# MAT-NSC & MAT-EN cannot be taught on the same day
# TODO: rewrite this to include lists instead of manually performing the cartesian product
problem.addConstraint(is_not_on_the_same_day, ('MAT1','MAT2','NSC1','NSC2','EN1','EN2'))

# All teachers must lecture different subjects
problem.addConstraint(constraint.AllDifferentConstraint(), [*teachers.keys()])

# FIXME: add function/constraint to take into account that lucia teaches hsc if andrea lectures pe
problem.addConstraint(lucia_teaches_hsc, ('LUC1','LUC2','AND1','AND2'))

# Juan won't teach any of the sciences if it is at first hour on mondays or thursdays
# TODO: rewrite this to avoid calling the function 2 times
problem.addConstraint(juan_can_teach, ('JUA1','JUA2','NSC1','NSC2','HSC1','HSC2'))

print_solution(problem.getSolutions())