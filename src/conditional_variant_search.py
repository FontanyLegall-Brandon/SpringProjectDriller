import os
import subprocess
import xlsxwriter
import csv

def setup_excel_file():
    worksheet = workbook.add_worksheet()
    worksheet.write(0, 0,"Project Name")
    worksheet.write(0, 1, "@Conditional(")
    worksheet.write(0, 2,  "@ConditionalOnProperty(")
    worksheet.write(0, 3,  "@ConditionalOnMissingBean(")
    worksheet.write(0, 4, "@ConditionalOnAdmin(")
    worksheet.write(0, 5,  "@ConditionalOnBean(")
    worksheet.write(0, 6, "@ConditionalOnClass(")
    worksheet.write(0, 7, "@ConditionalOnMissingClass(")
    worksheet.write(0, 8, "Personalise @Conditional")

    return worksheet

def clone(repo_url):
    os.system('cd ../repository_cache/ ; git clone ' + repo_url)

def init_variants_dico():
    dico = {}

    for variant in conditional_variants:
        dico[variant] = 0

    return dico


def clone_and_search_occurence(repo_input):
    row = 1

    for repo in repo_input:

        project_name = repo[repo.rfind('/')+1:repo.rfind('.')]
        variants_dico = init_variants_dico()
        clone(repo)
        for variant in conditional_variants :
            variants_dico[variant] += int(subprocess.check_output('grep -r \"' + variant + '\" ../repository_cache/*/* | wc -l ', shell=True).decode())
        projects_variants[project_name] = variants_dico


        index_in_row = 0
        total_number_without_simple_cond = 0

        for variant in conditional_variants:
            if (index_in_row > 0):
                total_number_without_simple_cond = total_number_without_simple_cond + variants_dico[variant]
            worksheet.write(row,index_in_row+1,variants_dico[variant])
            index_in_row = index_in_row +1

        #number of personnalise @conditionnal
        worksheet.write(row, index_in_row + 1,  int(subprocess.check_output('grep -r \"@Conditional[A-Za-z]+(\" ../repository_cache/*/* | wc -l ',shell=True).decode())-total_number_without_simple_cond)
        os.system('rm -rf ../repository_cache/' + project_name)
        row = row + 1
    return projects_variants

if __name__ == '__main__' :
    projects_variants = {}
    workbook = xlsxwriter.Workbook('../stats/occurence_variant.xlsx')
    conditional_variants = ["@Conditional(",
                            "@ConditionalOnProperty(",
                            "@ConditionalOnMissingBean(",
                            "@ConditionalOnAdmin(",
                            "@ConditionalOnBean(",
                            "@ConditionalOnClass(",
                            "@ConditionalOnMissingClass("]
    worksheet = setup_excel_file()
    finput = open("../project_url/repos_url.txt", "r")
    # Set an array with all repo url
    repo_input = [line.strip() for line in finput]
    print(repo_input)
    # Close the file
    finput.close()
    print(clone_and_search_occurence(repo_input))
    workbook.close()