from constraint import *

mon = range(0,3)
tue = range(4,7)
wed = range(8,11)
thu = range(12,14)

NSC = ['NSC1, NSC2']
HSC = ['HSC1', 'HSC2']
SP = ['SP1', 'SP2']
MAT = ['MAT1', 'MAT2']
EN = ['EN1', 'EN2']
PE = 'PE'

dict =	{
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
  'PE': [0, 1, 2, 4, 5, 6, 8, 9, 10, 12, 13],
}

def isConsecutive(a, b):
	return a + 1 == b or a == b + 1

def isOnTheSameDay(a, b):
	if a in mon:
		return b == mon
	elif a in tue:
		return b == tue
	elif a in wed:
		return b == wed
	elif a in thu:
		return b == thu
	else:
		return False

problem = Problem()

problem.addVariables([*dict.keys()], [*dict.values()])

# All subjects must be in different time slots
problem.addConstraint(AllDifferentConstraint(), [*dict.keys()])

# Natural science class must be consective
problem.addConstraint(isConsecutive, ('NSC1', 'NSC2'))

# MAT-NSC & MAT-SP cannot be taught in the same day
problem.addConstraint(isOnTheSameDay, (MAT, NSC))
problem.addConstraint(isOnTheSameDay, (MAT, SP))

print(problem.getSolution())





