import os
import re

def diff_stats(directory_in, directory_out, file_out):
    try:
        os.mkdir(directory_out)
    except OSError:
        print("Creation of the directory %s failed" % directory_out)
    with open(directory_out + file_out, mode='w') as output:
        for filename in os.listdir(directory_in):
            if filename.endswith(".txt"):
                conditionalInCounter = 0
                conditionalOutCounter = 0
                profileInCounter = 0
                profileOutCounter = 0

                with open(directory_in + filename) as file:


                    conditionalInRegex = re.compile(r"^\+.*@Conditional.*$")
                    conditionalOutRegex = re.compile(r"^\-.*@Conditional.*$")
                    profileInRegex = re.compile(r"^\+.*@Profile.*$")
                    profileOutRegex = re.compile(r"^\-.*@Profile.*$")

                    for line in file:
                        if profileInRegex.match(line):
                            profileInCounter += 1
                        if profileOutRegex.match(line):
                            profileOutCounter += 1
                        if conditionalInRegex.match(line):
                            conditionalInCounter += 1
                        if conditionalOutRegex.match(line):
                            conditionalOutCounter += 1

                output.write("{} | {} | {} | {} | {}\n".format(
                    filename,
                    profileInCounter,
                    profileOutCounter,
                    conditionalInCounter,
                    conditionalOutCounter
                ))
            else:
                continue

if __name__ == '__main__':
    diff_stats("../rimel-data-set/spring-boot-conditional-diff/", "../rimel-data-set/spring-boot-conditional-diff-stats/", "total.txt")