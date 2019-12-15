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
    'PE1': all_hours,
    'PE2': all_hours,
    'EN': all_hours
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


def is_not_on_the_same_day(a, b, c, d, e):
    """
    Check that no Natural Science or English class is on the same day as Math.

    :param a: time slot for any of the Math hours
    :param b: time slot for the other Math class
    :param c: time slot for any of the Natural Science classes
    :param d: time slot for the other Natural Science class
    :param e: time slot for the English classes
    """
    is_a_valid_instance = True

    for day in days:
        if a in day or b in day:
            is_a_valid_instance = is_a_valid_instance and c not in day and d not in day and e not in day

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
    :param i: first hour of EN class (PE1)
    :param j: second hour of EN class (PE2)
    """
    return a < b and c < d and e < f and g < h and i < j


def no_duplicated_teachers(a, b, c, d, e, f):
    """
    Avoid duplicating solutions with the same subject assignment but different order (analogous of
    no_duplicated_subjects() but for teachers).

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


def pe_is_not_on_the_same_day(a, b):
    """
    New added constrain to avoid both hours of EN to be on the same day

    :param a: first hour of PE class (PE1)
    :param b: second hour of PE class (PE2)
    """
    is_a_valid_instance = True

    for day in days:
        if a in day:
            is_a_valid_instance = is_a_valid_instance and b not in day

    return is_a_valid_instance


def juan_can_teach(a, b, c, d):
    """Check that Juan is able to teach HSC or NSC based on the constraints in the document

        Keyword arguments:
        a -- any of the subjects assigned to Juan
        b -- the other subject assigned to Juan
        c -- time slot for any of the Human Sciences class
        d -- time slot for the other Human Sciences class
    """
    if c in first_hours and (c in monday or c in thursday) or d in first_hours and (d in monday or d in thursday):
        return a != HSC and b != HSC
    return True


def print_solution(solution):
    """
    Pretty-print the dictionary with the solution that python-constraint returns

    :param solution: dictionary containing all the variables of the problem with its instantiated value
    """
    # Sort the solution dict by value and store it in a list
    sorted_solution = sorted(solution.items(), key=lambda kv: kv[1])
    # Copy by value the sorted list
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

    print("{:6s} {:^10s} {:^10s} {:^10s} \n".format("11-12",
                                                    subjects_solution[2][0],
                                                    subjects_solution[5][0],
                                                    subjects_solution[8][0]))

    print("NSC: {}, HSC: {}, SP: {},  MAT: {},  EN: {},  PE: {}".format(teachers_solution[0][0],
                                                                        teachers_solution[1][0],
                                                                        teachers_solution[2][0],
                                                                        teachers_solution[3][0],
                                                                        teachers_solution[4][0],
                                                                        teachers_solution[5][0]))


problem = constraint.Problem()

# Insert all elements of both dictionaries with its corresponding domains into the python constraint problem
for key, value in subjects.items():
    problem.addVariable(key, value)

for key, value in teachers.items():
    problem.addVariable(key, value)

# Avoid duplication of solutions
problem.addConstraint(no_duplicated_subjects,
                      ('NSC1', 'NSC2', 'HSC1', 'HSC2', 'SP1', 'SP2', 'MAT1', 'MAT2', 'PE1', 'PE2'))
problem.addConstraint(no_duplicated_teachers, ('AND1', 'AND2', 'JUA1', 'JUA2', 'LUC1', 'LUC2'))

# All subjects must be in different time slots
problem.addConstraint(constraint.AllDifferentConstraint(), [*subjects.keys()])

# Human & social science class must be consecutive
problem.addConstraint(is_consecutive, ('HSC1', 'HSC2'))

# MAT-NSC & MAT-EN cannot be taught on the same day
problem.addConstraint(is_not_on_the_same_day, ('MAT1', 'MAT2', 'NSC1', 'NSC2', 'EN'))

# There can't be more than one class of english in the same day
problem.addConstraint(pe_is_not_on_the_same_day, ('PE1', 'PE2'))

# All teachers must lecture different subjects
problem.addConstraint(constraint.AllDifferentConstraint(), [*teachers.keys()])

# LUC will lecture HSC provided that AND takes care of PE
problem.addConstraint(lucia_teaches_hsc, ('LUC1', 'LUC2', 'AND1', 'AND2'))

# JUA won't teach HSC nor NSC if it is at first hour on mon or thu
# Since NSC is forced in an earlier constraint to be at the last hour we don't need to check it
problem.addConstraint(juan_can_teach, ('JUA1', 'JUA2', 'HSC1', 'HSC2'))

start = timer()
print(len(problem.getSolutions()))
end = timer()
print_solution(problem.getSolution())
print("Time elapsed: {}".format(end - start))
