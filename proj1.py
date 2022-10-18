import sys

from pysat.solvers import Glucose4
from pysat.card import CardEnc, EncType
from pysat.examples.rc2 import RC2
from pysat.formula import WCNF

from pprint import pprint

solver = RC2(WCNF())

# parsing the input
lines = sys.stdin.readlines()

def parse(lines):
    # initialize counter for ongoing line reading    
    lineCounter = 0
    
    # Line 1 - Number of units
    numUnits = int(lines[lineCounter].rstrip())
    lineCounter += 1
    
    
    # Line 2 - Number of periods
    numPeriods = int(lines[lineCounter].rstrip())
    lineCounter += 1
    
    
    # Line 3 - Area size of each unit
    tempAreaSizes = lines[lineCounter].rstrip().split()
    areaSizes = [int(tempAreaSizes[i]) for i in range(len(tempAreaSizes))]
    lineCounter += 1
    
    
    # Line 4 to 4+n - Sequence of lines of adjacents units of each unit in corresponding line
    startAdjacents = lineCounter
    endAdjacents = lineCounter + numUnits
    
    adjacents = []
    for i in range(startAdjacents, endAdjacents):
        line = lines[i].rstrip().split()
        adjacents.append([int(line[i]) for i in range(len(line))])
    lineCounter = endAdjacents
        
    # Line 4+n to 4+n +numPeriods - Sequence of profits for each unit in corresponding period
    startPeriods = lineCounter
    endPeriods = lineCounter + numPeriods
    
    profits = []
    for i in range(startPeriods, endPeriods):
        line = lines[i].rstrip().split()
        profits.append([int(line[i]) for i in range(len(line))])
    lineCounter = endPeriods
    
    # Last line - Minimum area size for the natural reserve
    minArea = lines[-1]
    
    return numUnits, numPeriods, areaSizes, adjacents, profits, minArea
    
# Parse the input file
numUnits, numPeriods, areaSizes, adjacents, profits, minArea = parse(lines)

# Check the input parameters
# print('numUnits:', numUnits)
# print('numPeriods:', numPeriods)
# print('areaSizes:', areaSizes)
# print('adjacents:', adjacents)
# print('profits:', profits)
# print('minArea:', minArea)

# variable is unit i harvested in period g
# unit i with adjacent unit j
# 

# Define the variables
## X_ik -> Unit i is harvested in period k
## ## Y_ij -> Unit i is adjacent to unit j -> not necessary
## ## A_ia -> Unit i has area a -> not necessary
## Z_i -> Unit i belongs to natural reserve

# Create X_ik -> Unit i is harvested in period k
X_vars = []
for i in range(1, numUnits+1):
    # print(i)
    for k in range(1, numPeriods+1):
        X_vars.append('X_' + str(i) + '_' + str(k))
        
# pprint(X_vars)
# print('len X_vars:', len(X_vars))
# print('len X_vars / 3:', len(X_vars)/3)

# add constraint 1
# each unit is harvested at most once in the T time periods
# define the clauses
harvested = [[int(numPeriods*i+1 + j) for j in range(numPeriods)] for i in range(numUnits)]
# do the pairwise encoding
for i in range(numUnits):
    enc = CardEnc.atmost(lits = harvested[i], bound = 1, top_id = harvested[i][-1], encoding = EncType.pairwise)
    for clause in enc.clauses:
        # print('adding clause:', clause)
        solver.add_clause(clause)


# Constraint 2: two adjacent units cannot be harvested in the same time period
# Xit -> not(Xkt), i U, t T, k adjacents[i]
for t in range(1, numPeriods+1):
    for unit in range(1, numUnits+1):
        for adj in range(1, len(adjacents[unit-1])):
            clause = [-(unit*t), -(adjacents[unit-1][adj]*t)]
            # print('adding clause:', clause)
            solver.add_clause(clause)


# Profit optimization -> adding the soft clauses
## define the literals
literals = [int(x+1) for x in range(numPeriods*numUnits)]

## add soft clauses
# adding the soft clauses
literals = [int(x+1) for x in range(numPeriods*numUnits)]
for xij in literals:
    column = ((xij-1)//numPeriods)
    row = ((xij-1)%numPeriods)
    # print('xij:', xij)
    # print('column:', column)
    # print('row:', row)
    # print('adding clause:', [xij], profits[row][column])
    solver.add_clause([xij], weight = profits[row][column])
    # print('----')
    
# Solve the problem statement
model = solver.compute()
cost = solver.cost
# print("Model:", model)
# print('Cost:', cost)

# Translate the model back to vars
## Define function for translation
def explain_model(model, X_vars):
    attrs = X_vars
    if model != None:
        print("\nTrue literals are:")
        for v in model:
            if int(v) > 0:
                print('id:', (v)-1)
                print(attrs[int(v)-1], '\n')

## translate back with defined function
# explain_model(model, X_vars)


