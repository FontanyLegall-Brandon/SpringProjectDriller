import re

import xlsxwriter

from pydriller import RepositoryMining, GitRepository

def setup_excel_file_2010():
    worksheet = workbook.add_worksheet()
    worksheet.write(0, 0,"Project Name")
    worksheet.write(0, 1, " 2010")
    worksheet.write(0, 2, " 2011")
    worksheet.write(0, 3, " 2012")
    worksheet.write(0, 4, " 2013")
    worksheet.write(0, 5, " 2014")
    worksheet.write(0, 6, " 2015")
    worksheet.write(0, 7, " 2016")
    worksheet.write(0, 8, " 2017")
    worksheet.write(0, 9, " 2018")
    worksheet.write(0, 10, " 2019")
    return worksheet

def setup_excel_file_2013():
    worksheet = workbook.add_worksheet()
    worksheet.write(0, 0,"Project Name")
    worksheet.write(0, 3, " 2013")
    worksheet.write(0, 4, " 2014")
    worksheet.write(0, 5, " 2015")
    worksheet.write(0, 6, " 2016")
    worksheet.write(0, 7, " 2017")
    worksheet.write(0, 8, " 2018")
    worksheet.write(0, 9, " 2019")
    return worksheet

def setup_excel_file_2016():
    worksheet = workbook.add_worksheet()
    worksheet.write(0, 0,"Project Name")
    worksheet.write(0, 6, " 2016")
    worksheet.write(0, 7, " 2017")
    worksheet.write(0, 8, " 2018")
    worksheet.write(0, 9, " 2019")
    return worksheet

def remove_comments(java_class):
    comments_regex = re.compile(r"//.*")
    multi_line_comments = re.compile(r"""((['"])(?:(?!\2|\\).|\\.)*\2)|\/\/[^\n]*|\/\*(?:[^*]|\*(?!\/))*\*\/""")

    java_class = re.sub(multi_line_comments,'',  java_class)
    return re.sub(comments_regex,'', java_class)

def find_occurence_in_commit(commit, word):
    conditional_added = 0
    for m in commit.modifications:
        tmp = remove_comments(str(m.diff))
        conditional_added = conditional_added + tmp.count(word)

    return conditional_added


def explore_commits(repo_input):
    row = 1
    column_project_name = 0
    column_conditional = 1
    column_profile = 2

    #pour tous les projets github
    for repo in repo_input :
        nb_commit = 0
        occurences = [0 for x in range(10)]
        conditional_added = 0
        #pour tous les commit dans ces projets
        print(repo)

        for commit in RepositoryMining(repo, only_modifications_with_file_types=['.java']).traverse_commits():
            if(nb_commit == 0):
                if (int(str(commit.committer_date)[0:4]) < 2013):
                    worksheet = worksheet2010
                    worksheet.write(row, 0, repo[repo.rfind('/'):repo.rfind('.')])
                if (int(str(commit.committer_date)[0:4]) < 2016):
                    worksheet = worksheet2013
                    worksheet.write(row, 0, repo[repo.rfind('/'):repo.rfind('.')])
                else :
                    worksheet = worksheet2016
                    worksheet.write(row, 0, repo[repo.rfind('/'):repo.rfind('.')])

            if(int(str(commit.committer_date)[0:4])>=2010) :
                # on récupere le nombre de conditional ajouté dans le commit et on l'ajoute au  nombre total de conditional
                occurences[int(str(commit.committer_date)[3])] = occurences[int(str(commit.committer_date)[3])] + find_occurence_in_commit(commit, word)

            nb_commit = nb_commit + 1
        for i in range(9):
            worksheet.write(row,i+1,occurences[i+1])


        row = row + 1


if __name__ == '__main__' :
    word ="@Conditional"
    workbook = xlsxwriter.Workbook('../stats/stats_occurence_in_year_in_function_of_creation_date'+word+'.xlsx')
    worksheet2010 = setup_excel_file_2010()
    worksheet2013 = setup_excel_file_2013()
    worksheet2016 = setup_excel_file_2016()
    #get in repos_url.txt all the the github to explore
    f = open("../project_url/repos_url.txt", "r")
    #Set an array with all repo url
    repo_input = [line.strip() for line in f]
    #Close the file
    f.close()
    explore_commits(repo_input)
    workbook.close()

