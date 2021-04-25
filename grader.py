import subprocess
import shutil


for i in range(1, 51):
    shutil.copy("tests/grade/input_" + str(i) + ".txt", "input.txt")
    # subprocess.run(["cp", "input_" + str(i) + ".txt", "input.txt"])
    subprocess.run(["python", "homework.py"])
    my_output = ''
    with open('output.txt') as ipfile:
        my_output = ipfile.read()
    theirs = ''
    with open('tests/grade/output_' + str(i) + '.txt') as ipfile:
        theirs = ipfile.read()

    print("Test case", i, ":", my_output == theirs)
