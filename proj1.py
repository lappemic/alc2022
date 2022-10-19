import sys

from pysat.card import CardEnc, EncType
from pysat.examples.rc2 import RC2
from pysat.formula import WCNF

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
    minArea = int(lines[-1])
    
    return numUnits, numPeriods, areaSizes, adjacents, profits, minArea
    
# Parse the input file
numUnits, numPeriods, areaSizes, adjacents, profits, minArea = parse(lines)

# add constraint 1
# each unit is harvested at most once in the T time periods
# define the clauses
harvested = [[int(numPeriods*i+1 + j) for j in range(numPeriods)] for i in range(numUnits)]
# do the pairwise encoding
for i in range(numUnits):
    enc = CardEnc.atmost(lits = harvested[i], bound = 1, top_id = harvested[i][-1], encoding = EncType.pairwise)
    for clause in enc.clauses:
        solver.add_clause(clause)


# Constraint 2: two adjacent units cannot be harvested in the same time period
# Xit -> not(Xkt), i U, t T, k adjacents[i]
literals = [int(x+1) for x in range(numPeriods*numUnits)]
for Lij in literals:
    c = (((Lij)-1)%numPeriods)+1
    u = (Lij-1)//numPeriods

    #It starts at 1, because the 0 is the number of adjs
    for adj in range(1, adjacents[u][0] + 1):
        r = adjacents[u][adj] 
        clause = [-(Lij), -((r-1)*numPeriods + c)]
        solver.add_clause(clause)


# Profit optimization -> adding the soft clauses
## add soft clauses
for xij in literals:
    column = ((xij-1)//numPeriods)
    row = ((xij-1)%numPeriods)
    solver.add_clause([xij], weight = profits[row][column])
    
# Solve the problem statement
model = solver.compute()
cost = solver.cost

# Calculate the effective profit
## take just the positive numbers
modelPos = [x for x in model if x > 0]

## calculate the maximal profit as well as the units harvested in each period
maxProfit = 0
periods = []
units = []
for xij in modelPos:

    # get maximal profit
    column = ((xij-1)//numPeriods)
    row = ((xij-1)%numPeriods)
    maxProfit += profits[row][column]
    
    # get unit i harvested in period j
    period = ((xij-1)%numPeriods)
    unit = ((xij-1)//numPeriods)
    periods.append(period+1)
    units.append(unit+1)

# Define the ouput
## Profit
print(maxProfit)

## create prints of the k lines with jth line containing nr and identifiers of harvested units in kth period
for per in set(periods):
    idxj = [i for i, x in enumerate(periods) if x == per]
    harvUnitsPeriod = [units[x] for x in idxj]
    
    # print the resulting line
    print(len(harvUnitsPeriod), *harvUnitsPeriod)

## if minArea of natural reserve is 0 print it
if minArea == 0:
    print(minArea)