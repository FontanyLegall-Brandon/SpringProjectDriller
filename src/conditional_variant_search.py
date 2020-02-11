import os
import subprocess
import xlsxwriter
import csv

def clone(repo_url):
    os.system('cd ../repository_cache/ ; git clone ' + repo_url)

def init_variants_dico():
    dico = {}

    for variant in conditional_variants:
        dico[variant] = 0

    return dico


def clone_and_search_occurence(repo_input):



    for repo in repo_input:

        project_name = repo[repo.rfind('/')+1:repo.rfind('.')]
        variants_dico = init_variants_dico()
        clone(repo)
        for variant in conditional_variants :
            variants_dico[variant] += int(subprocess.check_output('grep -r \"' + variant + '\" ../repository_cache/*/* | wc -l ', shell=True).decode())
        projects_variants[project_name] = variants_dico
        os.system('rm -rf ../repository_cache/'+ project_name)
    return projects_variants

if __name__ == '__main__' :
    projects_variants = {}
    conditional_variants = ["@Conditional(",
                            "@ConditionalOnProperty(",
                            "@ConditionalOnMissingBean(",
                            "@ConditionalOnAdmin(",
                            "@ConditionalOnBean(",
                            "@ConditionalOnClass(",
                            "@ConditionalOnMissingClass("]
    finput = open("../project_url/repos_url.txt", "r")
    # Set an array with all repo url
    repo_input = [line.strip() for line in finput]
    print(repo_input)
    # Close the file
    finput.close()
    print(clone_and_search_occurence(repo_input))