import subprocess
import shutil
import time


test_cats = ["./tests", "./tests/grade", "./tests/testcase"]


def run_grade():
    num_tests = 50
    passed = 0
    failed = []
    for i in range(1, num_tests + 1):
        shutil.copy("tests/grade/input_" + str(i) + ".txt", "input.txt")
        subprocess.run(["python", "homework.py"])
        my_output = ''
        with open('output.txt') as ipfile:
            my_output = ipfile.read()
        theirs = ''
        with open('tests/grade/output_' + str(i) + '.txt') as ipfile:
            theirs = ipfile.read()

        if my_output == theirs:
            passed += 1
        else:
            failed.append(i)
        print("Test case", i, ":", my_output == theirs)
    print("Passed: {}/{}".format(passed, num_tests))
    if failed:
        print("Failed #s:\n{}".format(failed))
        return failed
    return []


def run_tests():
    num_tests = 21
    passed = 0
    failed = []
    for i in range(1, num_tests + 1):
        file_no_str = None
        if i < 10:
            file_no_str = "0" + str(i)
        else:
            file_no_str = str(i)
        shutil.copy("tests/input_" + file_no_str + ".txt", "input.txt")
        subprocess.run(["python", "homework.py"])
        my_output = ''
        with open('output.txt') as ipfile:
            my_output = ipfile.read()
        theirs = ''
        with open('tests/output_' + file_no_str + '.txt') as ipfile:
            theirs = ipfile.read()

        if my_output == theirs:
            passed += 1
        else:
            failed.append(i)
        print("Test case", i, ":", my_output == theirs)
    print("Passed: {}/{}".format(passed, num_tests))
    if failed:
        print("Failed #s:\n{}".format(failed))
        return failed
    return []


def run_testcase():
    num_tests = 33
    passed = 0
    failed = []
    for i in range(1, num_tests + 1):
        shutil.copy("tests/testcase/input" + str(i) + ".txt", "input.txt")
        subprocess.run(["python", "homework.py"])
        my_output = ''
        with open('output.txt') as ipfile:
            my_output = ipfile.read()
        theirs = ''
        with open('tests/testcase/output' + str(i) + '.txt') as ipfile:
            theirs = ipfile.read().rstrip("\n")

        if my_output == theirs:
            passed += 1
        else:
            failed.append(i)
        print("Test case", i, ":", my_output == theirs)
    print("Passed: {}/{}".format(passed, num_tests))
    if failed:
        print("Failed #s:\n{}".format(failed))
        return failed
    return []


def run_test_cats(cats):
    ret = []
    if 1 in cats:
        ret.append(run_tests())
    if 2 in cats:
        ret.append(run_grade())
    if 3 in cats:
        ret.append(run_testcase())
    return ret


start_time = time.time()
ret = run_test_cats([1, 2, 3])

if ret:
    print("Failed cases:\n" + str(ret))
end_time = time.time()
print("Total time taken to run all test cases:\n{} seconds".format(
    end_time - start_time))
