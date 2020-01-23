import os
import subprocess
import xlsxwriter
import csv


def setup_excel_file():
    worksheet = workbook.add_worksheet()
    worksheet.write(0, 0,"Project Name")
    worksheet.write(0, 1, "@Conditional")
    worksheet.write(0, 2, "@Profile")
    return worksheet

def clone_and_search_occurence(repo_input):

    row = 1
    column_project_name = 0
    column_conditional = 1
    column_profile = 2
    for line in repo_input:
        project_name = line[line.rfind('/')+1:line.rfind('.')]

        worksheet.write(row,column_project_name,project_name)
        os.system('cd repository_cache/ ; git clone '+line)
        occurence_contional = subprocess.check_output('grep -r \"@Conditional\" ./repository_cache/*/* | wc -l ', shell=True).decode()

        worksheet.write(row, column_conditional, int(occurence_contional))
        occurence_profile = subprocess.check_output('grep -r \"@Profil\" ./repository_cache/*/* | wc -l ', shell=True).decode()
        worksheet.write(row, column_profile, int(occurence_profile))
        os.system('rm -rf repository_cache/'+ project_name)
        data_list.append([project_name,int(occurence_contional),int(occurence_contional)])
        row = row + 1


def file_cvs_with_array():
    with open('../stats/stats.csv', 'w', newline='') as file:
        writer = csv.writer(file, delimiter='|')
        writer.writerows(data_list)

if __name__ == '__main__' :
    workbook = xlsxwriter.Workbook('../stats/stat.xlsx')
    data_list = [["Project Name","@Conditional","@Profil"]]
    worksheet = setup_excel_file()
    finput = open("../project_url/repos_url.txt", "r")
    # Set an array with all repo url
    repo_input = [line.strip() for line in finput]
    print(repo_input)
    # Close the file
    finput.close()
    clone_and_search_occurence(repo_input)
    workbook.close()
    file_cvs_with_array()