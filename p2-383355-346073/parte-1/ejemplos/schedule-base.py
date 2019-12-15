import constraint
from timeit import default_timer as timer

# Each day is defined by the range denoted below, note the one-number-gap between days
monday = range(0, 3)
tuesday = range(4, 7)
wednesday = range(8, 11)
thursday = range(12, 14)

# List containing the ranges of every day of the week
days = [monday, tuesday, wednesday, thursday]

# List containing all possible hours to assign
all_hours = list(monday) + list(tuesday) + list(wednesday) + list(thursday)

# Lists with the first hour and last hour of each day
first_hours = [0, 4, 8, 12]
last_hours = [2, 6, 10, 13]

# Assign a number to each subject
NSC = 0
HSC = 1
SP = 2
MAT = 3
EN = 4
PE = 5

# List containing all subjects
all_subjects = [NSC, HSC, SP, MAT, EN, PE]

# Dictionary with all the variables regarding subjects and its corresponding domains
# Mon@1st = 0, Mon@2nd = 1, Mon@3rd = 2, Tue@1st = 4, ... , Thu@2nd = 13
subjects = {
    'NSC1': last_hours,
    'NSC2': last_hours,
    'HSC1': all_hours,
    'HSC2': all_hours,
    'SP1': all_hours,
    'SP2': all_hours,
    'MAT1': first_hours,
    'MAT2': first_hours,
    'EN1': all_hours,
    'EN2': all_hours,
    'PE': all_hours
}

# Dictionary with all the variables regarding teaches and its domains
teachers = {
    'LUC1': all_subjects,
    'LUC2': all_subjects,
    'AND1': all_subjects,
    'AND2': all_subjects,
    'JUA1': all_subjects,
    'JUA2': all_subjects
}


def is_consecutive(a, b):
    """
    Check if the time slots are consecutive

    :param a: time slot for the first subject
    :param b: time slot for the second subject
    """
    return b == a + 1 or a == b + 1


def is_not_on_the_same_day(a, b, c, d, e, f):
    """
    Check that no Natural Science or English class is on the same day as Math.

    :param a: time slot for any of the Math hours
    :param b: time slot for the other Math class
    :param c: time slot for any of the Natural Science classes
    :param d: time slot for the other Natural Science class
    :param e: time slot for any of the English classes
    :param f: time slot for the other English class
    """
    is_a_valid_instance = True

    for day in days:
        if a in day or b in day:
            is_a_valid_instance = is_a_valid_instance and c not in day and d not in day and e not in day and f not in day

    return is_a_valid_instance


def no_duplicated_subjects(a, b, c, d, e, f, g, h, i, j):
    """
    Avoid the duplication of solutions for interchangeable positions like MAT1-MAT2 (the two hours of the same subject)
    by forcing the first hour (XXX1) to be before the second one (XXX2), where XXX denote the name of the subject.

    :param a: first hour of NSC class (NSC1)
    :param b: second hour of NSC class (NSC2)
    :param c: first hour of HSC class (HSC1)
    :param d: second hour of HSC class (HSC2)
    :param e: first hour of SP class (SP1)
    :param f: second hour of SP class (SP2)
    :param g: first hour of MAT class (MAT1)
    :param h: second hour of MAT class (MAT2)
    :param i: first hour of EN class (EN1)
    :param j: second hour of EN class (EN2)
    """
    return a < b and c < d and e < f and g < h and i < j


def no_duplicated_teachers(a, b, c, d, e, f):
    """
    Avoid duplicating solutions with the same subject assignment but different order (analogous of
    no_duplicated_subjects() but for teachers.

    :param a: first subject for AND
    :param b: second subject for AND
    :param c: first subject for JUA
    :param d: second subject for JUA
    :param e: first subject for LUC
    :param f: second subject for JUA
    """
    return a < b and c < d and e < f


def lucia_teaches_hsc(a, b, c, d):
    """
    Check that Lucia teaches Human Sciences if Andrea is assigned Physical Education

    :param a: any of the subjects assigned to Lucia
    :param b: the other subject assigned to Lucia
    :param c: any of the subjects assigned to Andrea
    :param d: the other subject assigned to Andrea
    """
    if a == HSC or b == HSC:
        return c == PE or d == PE
    return True


def juan_can_teach(a, b, c, d):
    """
    Check that Juan is able to teach HSC or NSC based on the constraints in the document

    :param a: any of the subjects assigned to Juan
    :param b: the other subject assigned to Juan
    :param c: time slot for any of the Human Sciences class
    :param d: time slot for the other Human Sciences class
    """
    if c in first_hours and (c in monday or c in thursday) or d in first_hours and (d in monday or d in thursday):
        return a != HSC and b != HSC
    return True


def check_solutions(solutions):
    print("Checking the validity of the solutions...")

    errors_in_constraint_3 = 0
    errors_in_constraint_4 = 0
    errors_in_constraint_5 = 0
    errors_in_constraint_6 = 0
    errors_in_constraint_7 = 0
    errors_in_constraint_8 = 0

    for item in solutions:
        # Checking errors for statement 1
        # This constraint is implicit in our model, since each subject is assigned to a slot,
        # and our slots are defined as one-hour periods.

        # Checking errors for statement 2
        # This constraint is also included and tested in our variables choice, since PE only has one,
        # while the rest of the subjects have two variables.

        # Checking errors for statement 3
        if item['HSC1'] + 1 != item['HSC2'] and item['HSC2'] + 1 != item['HSC1']:
            errors_in_constraint_3 += 1
            print("Error in 3rd constraint")
            print_solution(item)

        # Checking errors for statement 4
        for day in days:
            if (item['MAT1'] in day or item['MAT2'] in day) and (
                    item['NSC1'] in day or item['NSC2'] in day or item['EN1'] in day or item['EN2'] in day):
                errors_in_constraint_4 += 1
                print("Error in 4th constraint")
                print_solution(item)

        # Checking errors for statement 5
        if item['MAT1'] not in first_hours and item['MAT2'] not in first_hours:
            errors_in_constraint_5 += 1
            print("Error in 5th constraint")
            print_solution(item)

        # Checking errors for statement 6
        if item['AND1'] != item['AND2'] != item['LUC1'] != item['LUC2'] != item['JUA1'] != item['JUA2']:
            continue
        else:
            errors_in_constraint_6 += 1
            print("Error in 6th constraint")
            print_solution(item)

        # Checking errors for statement 7
        if item['LUC1'] == HSC or item['LUC2'] == HSC:
            if item['AND1'] != PE and item['AND2'] != PE:
                errors_in_constraint_7 += 1
                print("Error in 7th constraint")
                print_solution(item)

        # Checking errors in statement 8
        precondition_for_8_hsc = (item['HSC1'] in first_hours or item['HSC2'] in first_hours) and \
                                 ((item['HSC1'] in monday or item['HSC2'] in monday) or
                                  (item['HSC1'] in thursday or item['HSC2'] in thursday))

        precondition_for_8_nsc = (item['NSC1'] in first_hours or item['NSC2'] in first_hours) and \
                                 ((item['NSC1'] in monday or item['NSC2'] in monday) or
                                  (item['NSC1'] in thursday or item['NSC2'] in thursday))

        if precondition_for_8_nsc:
            if item['JUA1'] == NSC or item['JUA2'] == NSC:
                errors_in_constraint_8 += 1
                print("Error in 8th constraint, NSC part")
                print_solution(item)

        if precondition_for_8_hsc:
            if item['JUA1'] == HSC or item['JUA2'] == HSC:
                errors_in_constraint_8 += 1
                print("Error in 8th constraint, HSC part")
                print_solution(item)

    sum_of_errors = errors_in_constraint_3 + errors_in_constraint_4 + errors_in_constraint_5 + errors_in_constraint_6 + errors_in_constraint_7 + errors_in_constraint_8
    if sum_of_errors == 0:
        print("No errors found")
    else:
        print("Found the following errors: 3: {}\n4: {}\n5: {}\n6: {}\n7: {}\n8: {}".format(errors_in_constraint_3,
                                                                                            errors_in_constraint_4,
                                                                                            errors_in_constraint_5,
                                                                                            errors_in_constraint_6,
                                                                                            errors_in_constraint_7,
                                                                                            errors_in_constraint_8))


def print_solution(solution):
    # Sort the solution from python-constraint by value and store it in a list
    sorted_solution = sorted(solution.items(), key=lambda kv: kv[1])
    # Copy by value the sorted list and create an empty one to store the teachers solutions only
    subjects_solution = sorted_solution[:]
    teachers_solution = []

    # For each item in the sorted solution, delete the keys containing any teacher assignment and populate the list
    # regarding teachers
    for slot in sorted_solution:
        slot_key = slot[0]
        slot_value = slot[1]

        if slot_key in teachers.keys():
            teachers_solution.append((slot_key, slot_value))
            subjects_solution.remove(slot)

    # Format the solution into a table to visualize it better
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


start = timer()
problem = constraint.Problem()

# Insert all elements of both dictionaries with its corresponding domains into the python constraint problem
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

check_solutions(problem.getSolutions())
end = timer()
print_solution(problem.getSolution())

print("Time elapsed: {}".format(end - start))
