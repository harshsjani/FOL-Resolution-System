import os
import sys
import subprocess


for i in range(1, 51):
    subprocess.run(["cp", "input_" + str(i) + ".txt", "input.txt"])
    subprocess.run(["python3", "homework3.py"])
    my_output = ''
    with open('output.txt') as ipfile:
        my_output = ipfile.read()
    theirs = ''
    with open('output_' + str(i) + '.txt') as ipfile:
        theirs = ipfile.read()

    print("Test case", i, ":", my_output == theirs)
    #break

