import pandas as pd
import numpy as np
from random import randint
from numba import jit
from numba.core import types
from numba.typed import Dict
from numba.core.types import unicode_type, float64
 
@jit(nopython=True)
def MakeMatrix(nRows):
    d = []
    for _ in range(nRows):
        d.append([0.0 for _ in range(nRows)])
    
    d = np.array(d)

    return d

@jit(nopython=True)
def RMSD(ref, other):
    return (((other - ref) ** 2).mean() ** 0.5)

@jit(nopython=True)
def CalculateRMSD(data, matrix, nRows, mem):
    for i in range(nRows):
        for j in range(nRows):
            key = str(min(i, j)) + ", " + str(max(i, j))
            if key not in mem:
                mem[key] = RMSD(data[i], data[j])
            matrix[i][j] = mem[key]

    return matrix

@jit() #Everything until WriteToFile will execute in nopython mode, writing to a file shouldn't take too long
def FormatMatrix(matrix, fileName):
    """To be passed into cpptraj, the matrix has to be in a specific "melted" form.
    This takes an NxN matrix and converts it to the appropriate format.

    Args:
        matrix (pd.DataFrame): The dataframe to be converted. Must be NxN.

    Returns:
        None
    """

    # The data needs to go from being in a matrix to the following form:
    # #F1 F2 RMSD
    # [row number] [col number] [RMSD value]
    #
    # Where only values from the upper triangle are kept
    # I'm not sure if the column names need to be like this

    startIndex = 0
    toWrite = []
    toWrite.append("#F1 F2 RMSD\n")
    for rowNum, row in enumerate(matrix):
        for colNum, item in enumerate(row[startIndex:]):
            toWrite.append(f"{rowNum} {colNum + startIndex} {item}\n")
        startIndex += 1
    
    WriteToFile(toWrite, fileName)

def WriteToFile(data, fileName):
    with open(fileName, "w") as f:
        for line in data:
            f.write(line)

def Main():
    n = 10
    data = np.array([[randint(0, 9) for _ in range(n)] for _ in range(n)])
    mem = Dict.empty(
        key_type = unicode_type,
        value_type = float64
    )

    print(data)

    matrix = MakeMatrix(len(data))

    matrix = CalculateRMSD(data, matrix, len(data), mem)

    print(matrix)

    FormatMatrix(matrix, "test.dat")

if __name__ == "__main__":
    Main()