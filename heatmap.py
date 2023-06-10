#this file is used to display a heatmap of an area scan based off of average intensity, max intensity, or center of mass of the curve

import numpy as np
import seaborn as sns
import matplotlib.pylab as plt

counter1 = 0
counter2 = 0
method = 0
choice = 0
delim = " "
wavelengths = []
finalcomlist = []
finalavglist = []
finalmaxlist = []

userinput = input("Choose the method used for data storage (1 or 2): ")
if userinput == '1':
    method = 'spec'
    choice = 1
if userinput == '2':
    #change the method variable if needed to match your file name
    method = 'data'
    choice = 2

if choice == 1:
    #change this to match the file name of your x data if needed
    f1 = open("x-axis.txt", "r")

    for i in f1:
        l = float(f1.readline().strip())
        wavelengths.append(l)

if choice == 2:
    f1 = open(f"{method}_1_1.txt", "r")

    for i in f1:
        l = f1.readline().strip()
        res = delim.join(sorted(l.split()))

        wavelengths.append(float(res[0]))

while counter1 != 4 and counter2 != 4:
    for x in range(0, 4):
        comlist = []
        averagelist = []
        maxlist = []
        counter2 = 0
        for x in range(0, 4):
            result1 = 0
            result2 = 0
            counter3 = 0
            average = 0
            maximum = 0
            inputlist = []
            com = 0
            if choice == 1:
                filename = (f"{method}_{counter1}_{counter2}.txt")
            if choice == 2:
                filename = (f"{method}_{counter1 + 1}_{counter2 + 1}.txt")
            
            f2 = open(filename, "r")

            for i in f2:
                if choice == 1:
                    inputnum = float(f2.readline().strip())
                    inputlist.append(inputnum)
                if choice == 2:
                    l = f2.readline().strip()
                    res = delim.join(sorted(l.split()))

                    inputlist.append(float(res[1]))

            #calculate average
            for x in inputlist:
                average += x

            average = average / len(inputlist)

            #calculate maximum
            maximum = max(inputlist)

            #calculate center of mass
            for x in inputlist:
                result1 += (x * wavelengths[counter3])
                counter3 += 1

            for x in inputlist:
                result2 += (x * 0.157)

            com = result1 / result2

            comlist.append(com)
            averagelist.append(average)
            maxlist.append(maximum)

            counter2 += 1
        
        finalcomlist.append(comlist)
        finalavglist.append(averagelist)
        finalmaxlist.append(maxlist)
        counter1 += 1

 

userinput = input("Which heatmap you like to see?\n1) Center of Mass\n2) Average\n3) Maximum\n")
if userinput == '1':
    ax = sns.heatmap(finalcomlist, linewidth=0)
if userinput == '2':
    ax = sns.heatmap(finalavglist, linewidth=0)
if userinput == '3': 
    ax = sns.heatmap(finalmaxlist, linewidth=0)
plt.show()