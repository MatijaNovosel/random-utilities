import sys

file1Name = sys.argv[1]
file2Name = sys.argv[2]
outputFileName = "output.txt"

try:
    with open(file1Name, "r") as file1, open(file2Name, "r") as file2, open(
        outputFileName, "w"
    ) as outputFile:
        outputFileLines = []
        file1Lines = file1.readlines()
        file2Lines = file2.readlines()

        for line in file2Lines:
            if line not in file1Lines:
                outputFileLines.append(line)

        outputFile.writelines(outputFileLines)
except IOError as e:
    print(f"Operation failed: {e.strerror}")
