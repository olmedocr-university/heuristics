import constraint

mon = range(0, 3)
tue = range(4, 7)
wed = range(8, 11)
thu = range(12, 14)

days = [mon, tue, wed, thu]

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
    return b == a + 1 or a == b + 1


def is_not_on_the_same_day(a, b, c, d, e, f):
    is_a_valid_instance = True

    for day in days:
        if a in day or b in day:
            is_a_valid_instance = is_a_valid_instance and c not in day and d not in day and e not in day and f not in day

    return is_a_valid_instance


def no_duplicated_subjects(a, b, c, d, e, f, g, h, i, j):
    return a < b and c < d and e < f and g < h and i < j


def no_duplicated_teachers(a, b, c, d, e, f):
    return a < b and c < d and e < f


def lucia_teaches_hsc(a, b, c, d):
    if a == HSC or b == HSC:
        return c == PE or d == PE
    return True


def juan_can_teach(a, b, c, d):
    if c in first and (c in mon or c in thu) or d in first and (d in mon or d in thu):
        return a != HSC and b != HSC
    return True


def print_solution(solution):
    sorted_solution = sorted(solution.items(), key=lambda kv: kv[1])
    subjects_solution = sorted_solution[:]
    teachers_solution = []

    for slot in sorted_solution:
        slot_key = slot[0]
        slot_value = slot[1]

        if slot_key in teachers.keys():
            teachers_solution.append((slot_key, slot_value))
            subjects_solution.remove(slot)

    print("{:6s} {:^10s} {:^10s} {:^10s} {:^10s}".format("", "Mon", "Tue", "Wed", "Thu"))
    print("-" * 50)
    print("{:6s} {:^10s} {:^10s} {:^10s} {:^10s}".format("9-10",
                                                         subjects_solution[0][0],
                                                         subjects_solution[3][0],
                                                         subjects_solution[6][0],
                                                         subjects_solution[9][0]))

    print("{:6s} {:^10s} {:^10s} {:^10s} {:^10s}".format("10-11",
                                                         subjects_solution[1][0],
                                                         subjects_solution[4][0],
                                                         subjects_solution[7][0],
                                                         subjects_solution[10][0]))

    print("{:6s} {:^10s} {:^10s} {:^10s} {:^10s} \n".format("11-12",
                                                            subjects_solution[2][0],
                                                            subjects_solution[5][0],
                                                            subjects_solution[8][0],
                                                            ""))

    print("NSC: {}, HSC: {}, SP: {},  MAT: {},  EN: {},  PE: {}".format(teachers_solution[0][0],
                                                                        teachers_solution[1][0],
                                                                        teachers_solution[2][0],
                                                                        teachers_solution[3][0],
                                                                        teachers_solution[4][0],
                                                                        teachers_solution[5][0]))


problem = constraint.Problem()

for key, value in subjects.items():
    problem.addVariable(key, value)

for key, value in teachers.items():
    problem.addVariable(key, value)

# Avoid duplication of solutions
problem.addConstraint(no_duplicated_subjects,
                      ('NSC1', 'NSC2', 'HSC1', 'HSC2', 'SP1', 'SP2', 'MAT1', 'MAT2', 'EN1', 'EN2'))
problem.addConstraint(no_duplicated_teachers, ('AND1', 'AND2', 'JUA1', 'JUA2', 'LUC1', 'LUC2'))

# All subjects must be in different time slots
problem.addConstraint(constraint.AllDifferentConstraint(), [*subjects.keys()])

# Human & social science class must be consecutive
problem.addConstraint(is_consecutive, ('HSC1', 'HSC2'))

# MAT-NSC & MAT-EN cannot be taught on the same day
problem.addConstraint(is_not_on_the_same_day, ('MAT1', 'MAT2', 'NSC1', 'NSC2', 'EN1', 'EN2'))

# All teachers must lecture different subjects
problem.addConstraint(constraint.AllDifferentConstraint(), [*teachers.keys()])

# LUC will lecture HSC provided that AND takes care of PE
problem.addConstraint(lucia_teaches_hsc, ('LUC1', 'LUC2', 'AND1', 'AND2'))

# JUA won't teach HSC nor NSC if it is at first hour on mon or thu
# Since NSC is forced in an earlier constraint to be at the last hour we don't need to check it
problem.addConstraint(juan_can_teach, ('JUA1', 'JUA2', 'HSC1', 'HSC2'))

print_solution(problem.getSolution())
