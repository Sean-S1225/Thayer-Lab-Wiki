import pandas as pd
import numpy as np
from numba import jit, prange
from sys import argv
 
@jit(nopython=True)
def MakeMatrix(nRows):
    d = []
    for _ in range(nRows):
        d.append([0.0 for _ in range(nRows)])
    
    d = np.array(d, dtype=np.float16)

    return d

@jit(nopython=True)
def RMSD(ref, other):
    return (((other - ref) ** 2).mean() ** 0.5)

@jit(nopython=True, parallel=True)
def CalculateRMSD(data, matrix, nRows):
    startIndex = 0
    for i in prange(nRows):
        for j in prange(startIndex, nRows):
            rmsdVal = RMSD(data[i], data[j])
            matrix[i][j] = rmsdVal
            matrix[j][i] = rmsdVal

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

def Main(fileInput, fileOutput):
    data = pd.read_csv(fileInput, sep="\s+", dtype=np.float16).drop("#Frame", axis=1)
    dataLength = len(data)
    print(data)
    data = data.to_numpy()
    print(data)
    print(data)

    matrix = MakeMatrix(dataLength)

    matrix = CalculateRMSD(data, matrix, dataLength)

    print(matrix)

    FormatMatrix(matrix, fileOutput)

if __name__ == "__main__":
    Main(argv[1], argv[2])