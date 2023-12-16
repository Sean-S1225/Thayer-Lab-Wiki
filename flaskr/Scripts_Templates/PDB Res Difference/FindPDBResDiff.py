def FindDifferences(files: list[str]) -> None:
    """This function is used to identify differing residues in a PDB file. The location and differing residues will be printed.

    Args:
        files: a list of paths to files
    
    Returns:
        None
    """

    """
    Each meaningful line of the PDB file will look something like this:
    ATOM     15  H   VAL     2     -27.347  11.590   3.902  1.00  0.00
    [Type] [Atom Num] [Atom Type] [Residue Name] [Residue Number] [Coordinates]
    
    """
    residues = []
    
    for i in range(len(files)):
        currResidues = {}
        with open(files[i], "r") as file:
            for line in file.readlines():
                if line[:4] == "ATOM" and (line := line.split())[3] != "WAT": #If the line specifies an atom and isn't a water
                    currResidues[int(line[4])] = line[3]
        residues.append(currResidues)

    resKeysTemp = [list(x.keys()) for x in residues]
    resKeys = []
    for n in range(max([len(x) for x in resKeysTemp])):
        resKeys.append([x[n] if n < len(x) else None for x in resKeysTemp])

    print(*files)
    nameLengths = [len(file) for file in files]
    for keys in resKeys:
        zippedResidues = [residues[i][keys[i]] if keys[i] else None for i in range(len(keys))]
        equality = [zippedResidues[0] == x for x in zippedResidues]
        
        if False in equality:
            s = ""
            for fileVersion, nameLen in zip(zip(keys, zippedResidues), nameLengths):
                s += f"{str(fileVersion): <{nameLen-1}}| "
            print(s)

if __name__ == "__main__":
    # files = ["./p53_DBD_ff14SB_Rep1_WT_MarksFirstFrame.pdb", "./0.15_80_10_pH7_1tup_B.genpdb.cpptraj (1).pdb"]
    # files = ["./p53_DBD_ff14SB_Rep1_WT_MarksFirstFrame.pdb", "./0.15_80_10_pH7_1tup_B.genpdb.cpptraj (1).pdb"]
    # FindDifferences(files)

    files = ["./p53_DBD_ff14SB_Rep1_WT_MarksFirstFrame.pdb", "./p53_FL_DBD_ff19SB_Rep1_WT_PK11000_FirstFrame.pdb", "./p53_DBD_ff19SB_Rep1_WT_PK11000_FirstFrame.pdb"]
    FindDifferences(files)

    # print("\n" * 4)

    # files = ["./p53_DBD_ff14SB_Rep1_Y220C_MarksFirstFrame.pdb", "./p53_DBD_ff19SB_Y220C_Rep1_lastframe.pdb"]
    # FindDifferences(files)

    # print("\n" * 4)

    # files = ["./p53_DBD_ff14SB_Rep1_PK11000_MarksFirstFrame.pdb", "./p53_DBD_ff19SB_PK11000_Rep1_lastframe.pdb"]
    # FindDifferences(files)