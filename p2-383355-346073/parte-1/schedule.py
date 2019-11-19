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


def is_not_on_the_same_day(a, b, c, d, e, f):
    days = [mon, tue, wed, thu]
    for i in [a, b]:
        for j in days:
            if i in j:
                for k in [c, d, e, f]:
                    if k in j:
                        return False
    return True


def lucia_teaches_hsc(a, b, c, d):
    loop1 = False
    debug = [c, d]
    for i in [c, d]:
        loop1 = loop1 or i == PE
    loop2 = False
    for i in [a, b]:
        loop2 = loop2 or i == HSC
    return (loop1 and loop2) or (not loop1 and not loop2)


def juan_can_teach(a, b, c, d, e, f):
    for i in [a, b]:
        if i == NSC or i == HSC:
            for k in [c, d, e, f]:
                if (k in mon or k in thu) and k in first:
                    return False
    return True


def print_solution(solution):
    # TODO: write the method to beauty print the results

    print("Number of solutions found: {}\n".format(len(solution)))

    print("Checking the validity of the solutions...")
    number_of_errors_in_constraint_7 = 0
    number_of_errors_in_constraint_8 = 0
    for item in solution:
        valid_nsc_case = (item['HSC1'] in first or item['HSC2'] in first) and (
                (item['HSC1'] in mon or item['HSC2'] in mon) or (item['HSC1'] in thu or item['HSC2'] in thu))

        valid_hsc_case = (item['NSC1'] in first or item['NSC2'] in first) and (
                (item['NSC1'] in mon or item['NSC2'] in mon) or (item['NSC1'] in thu or item['NSC2'] in thu))

        valid_pe_case = item['AND1'] == PE or item['AND2'] == PE

        if valid_pe_case:
            invalid_item = item['LUC1'] != HSC and item['LUC2'] != HSC
            if invalid_item:
                number_of_errors_in_constraint_7 += 1
                print("Error in 7th constraint")
                print(item, '\n')

        if valid_nsc_case:
            invalid_item = item['JUA1'] == NSC or item['JUA2'] == NSC
            if invalid_item:
                number_of_errors_in_constraint_8 += 1
                print("Error in 8th constraint, NSC part")
                print(item, '\n')

        if valid_hsc_case:
            invalid_item = item['JUA1'] == HSC or item['JUA2'] == HSC
            if invalid_item:
                number_of_errors_in_constraint_8 += 1
                print("Error in 8th constraint, HSC part")
                print(item, '\n')

    if number_of_errors_in_constraint_7 + number_of_errors_in_constraint_8 != 0:
        print("No errors found")
    else:
        print("Found {} errors regarding constraint 7 and {} from constraint 8".format(number_of_errors_in_constraint_7,
                                                                                       number_of_errors_in_constraint_8))


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
problem.addConstraint(is_not_on_the_same_day, ('MAT1', 'MAT2', 'NSC1', 'NSC2', 'EN1', 'EN2'))

# All teachers must lecture different subjects
problem.addConstraint(constraint.AllDifferentConstraint(), [*teachers.keys()])

problem.addConstraint(lucia_teaches_hsc, ('LUC1', 'LUC2', 'AND1', 'AND2'))

# Juan won't teach any of the sciences if it is at first hour on mondays or thursdays
problem.addConstraint(juan_can_teach, ('JUA1', 'JUA2', 'NSC1', 'NSC2', 'HSC1', 'HSC2'))

print_solution(problem.getSolutions())
