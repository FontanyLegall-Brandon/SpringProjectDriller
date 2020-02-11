import os
import subprocess
import xlsxwriter
import csv

def clone(repo_url):
    os.system('cd ../repository_cache/ ; git clone ' + repo_url)


def clone_and_search_occurence(repo_input):

    conditional_variants = ["@Conditional(",
                            "@ConditionalOnProperty(",
                            "@ConditionalOnMissingBean(",
                            "@ConditionalOnAdmin(",
                            "@ConditionalOnBean(",
                            "@ConditionalOnClass(",
                            "@ConditionalOnMissingClass("]
    for variant in conditional_variants:
        dico[variant] = 0
    for repo in repo_input:

        project_name = repo[repo.rfind('/')+1:repo.rfind('.')]
        clone(repo)
        for variant in conditional_variants :
            dico[variant] += int(subprocess.check_output('grep -r \"' + variant + '\" ../repository_cache/*/* | wc -l ', shell=True).decode())

        os.system('rm -rf ../repository_cache/'+ project_name)
    return dico

if __name__ == '__main__' :
    dico = {}
    finput = open("../project_url/repos_url.txt", "r")
    # Set an array with all repo url
    repo_input = [line.strip() for line in finput]
    print(repo_input)
    # Close the file
    finput.close()
    print(clone_and_search_occurence(repo_input))