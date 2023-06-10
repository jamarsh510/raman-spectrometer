import os

numX = 75
numY = 32

i = 0
j = 0
f = open("1 Export File (Y-Axis)","r")
while i < numX*numY:
    q = int(i/numX)
    r = int(i % numX)
    stringName = "spec_" + str(r) + "_" + str(q) + ".txt"
    f1 = open(stringName,"w")
    while j < 2000:
        input = f.readline()
        if j == 1999:
            input = input[0:12] #removes newline on last line
        f1.write(input)
        j = j + 1
    f1.close()
    i = i + 1
    j = 0
f.close()