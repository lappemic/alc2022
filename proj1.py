import sys
import numpy as np

from pysat.solvers import Glucose4
from pysat.card import CardEnc, EncType

from pprint import pprint



# parsing function 2
file = 'input.txt'

def parse2(file):
    # initialize counter for ongoing line reading
    with open(file, 'r') as f:
        lines = f.readlines()
        # print(lines)
        f.close()
    
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
    
    periods = []
    for i in range(startPeriods, endPeriods):
        line = lines[i].rstrip().split()
        periods.append([int(line[i]) for i in range(len(line))])
    lineCounter = endPeriods
    
    # Last line - Minimum area size for the natural reserve
    minArea = lines[-1]
    
    return numUnits, numPeriods, areaSizes, adjacents, periods, minArea
    
# Parse the input file
numUnits, numPeriods, areaSizes, adjacents, periods, minArea = parse2(file)

# Check the input parameters
print('numUnits:', numUnits)
print('numPeriods:', numPeriods)
print('areaSizes:', areaSizes)
print('adjacents:', adjacents)
print('periods:', periods)
print('minArea:', minArea)

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
print('len X_vars:', len(X_vars))
print('len X_vars / 3:', len(X_vars)/3)

# define variable to check if unit i is harvested already
def valid_harvesting_period(X_vars):
    '''
    Check if unit i is harvested in period k
    '''
    valid_harvesting = []
    for i in range(int(len(X_vars)/numPeriods)):
        print(i)
        
    
valid_harvesting_period(X_vars)