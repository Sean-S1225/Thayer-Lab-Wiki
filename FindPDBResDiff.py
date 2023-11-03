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

    numResidues = [max(list(x.keys())) for x in residues]

    for n in range(1, max(numResidues) + 1):
        zippedResidues = [x[n] if n in x else "" for x in residues]
        equality = [zippedResidues[0] == x for x in zippedResidues]
        
        if False in equality:
            print(f"{n}: {zippedResidues}")

if __name__ == "__main__":
    files = ["./1tup_PostTleap_Mark.pbd", "./1tup_PostTleap_Sean.pbd"]
    FindDifferences(files)