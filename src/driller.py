import xlsxwriter

from pydriller import RepositoryMining, GitRepository

def setup_excel_file():
    worksheet = workbook.add_worksheet()
    worksheet.write(0, 0,"Project Name")
    worksheet.write(0, 1, " 2011")
    worksheet.write(0, 2, " 2012")
    worksheet.write(0, 3, " 2013")
    worksheet.write(0, 4, " 2014")
    worksheet.write(0, 5, " 2015")
    worksheet.write(0, 6, " 2016")
    worksheet.write(0, 7, " 2017")
    worksheet.write(0, 8, " 2018")
    worksheet.write(0, 9, " 2019")
    return worksheet

def find_occurence_in_commit(commit, word,file):

    conditional_added = 0
    commit_with_conditional = []
    commit_with_removed_conditional = []

    for m in commit.modifications:

        if(str(m.source_code).find(word) != -1):

            file.write("************** date : "+str(commit.committer_date)+"*****************\n")
            diff =word
            gr = GitRepository('test-repos/test1')
            parsed_lines = gr.parse_diff(diff)


            if(len(parsed_lines['added'])>0):
                conditional_added = conditional_added + len(parsed_lines['added'])

            lines = str(m.source_code).splitlines()
            commit_with_conditional.append(m.new_path)

            for line in lines:
                if line.find(word) != -1 :
                    file.write("\t\tligne ajouté : {}\n".format(line))

            if (len(parsed_lines['deleted']) > 0):
                conditional_added = conditional_added + len(parsed_lines['deleted'])

            lines = str(m.source_code).splitlines()
            commit_with_removed_conditional.append(m.new_path)

            for line in lines:
                if line.find(word) != -1:
                    file.write("\t\tligne retiré : {}\n".format(line))

    if(len(commit_with_conditional) > 0):
        file.write(str(commit_with_conditional)+"\n\n")

    return conditional_added


def find_occurence_in_commit(commit, word):
    conditional_added = 0
    for m in commit.modifications:
        conditional_added = conditional_added + str(m.diff).count(word)

    return conditional_added


def explore_commits(repo_input):
    row = 1
    column_project_name = 0
    column_conditional = 1
    column_profile = 2

    #pour tous les projets github
    for repo in repo_input :

        occurences = [0 for x in range(10)]
        worksheet.write(row,0,repo[repo.rfind('/'):repo.rfind('.')])
        conditional_added = 0
        #pour tous les commit dans ces projets
        print(repo)
        for commit in RepositoryMining(repo, only_modifications_with_file_types=['.java']).traverse_commits():
            if(int(str(commit.committer_date)[0:4])>2010) :
                # on récupere le nombre de conditional ajouté dans le commit et on l'ajoute au  nombre total de conditional
                occurences[int(str(commit.committer_date)[3])] = occurences[int(str(commit.committer_date)[3])] + find_occurence_in_commit(commit, word)

        for i in range(9):
            worksheet.write(row,i+1,occurences[i+1])


        row = row + 1


if __name__ == '__main__' :
    word ="@Conditional"
    workbook = xlsxwriter.Workbook('../stats/stats_occurence_in_year_'+word+'.xlsx')
    worksheet = setup_excel_file()
    #get in repos_url.txt all the the github to explore
    f = open("../project_url/repos_url.txt", "r")
    #Set an array with all repo url
    repo_input = [line.strip() for line in f]
    #Close the file
    f.close()
    explore_commits(repo_input)
    workbook.close()

