import fileinput

from pydriller import RepositoryMining, GitRepository

def find_occurence_in_commit(commit, word,file):

    conditional_added = 0
    commit_with_conditional = []

    for m in commit.modifications:

        if(str(m.source_code).find(word) != -1):

            file.write("************** date : "+format(commit.committer_date)+"*****************\n")
            diff ='+'+word
            gr = GitRepository('test-repos/test1')
            parsed_lines = gr.parse_diff(diff)


            if(len(parsed_lines['added'])>0):
                conditional_added = conditional_added + len(parsed_lines['added'])

            lines = format(m.source_code).splitlines()
            commit_with_conditional.append(m.new_path)

            for line in lines:
                if line.find(word) != -1 :
                    file.write("\t\tligne ajouté : {}\n".format(line))

    if(len(commit_with_conditional) > 0):
        file.write(str(commit_with_conditional)+"\n\n")

    return conditional_added

def explore_commits(repo_input):

    #pour tous les projets github
    for repo in repo_input :
        #On créer un fichier
        repofilename = "output"+ repo[repo.rfind('/'):] + ".txt"
        #et on l'ouvre en ecriture
        file = open(repofilename, 'w+')
        #compteur du nombre de conditionnal
        conditional_added = 0
        file.write("\n\n ***** le git du projet : {} *****\n".format(repo))
        #pour tous les commit dans ces projets
        for commit in RepositoryMining(repo).traverse_commits():
            #on récupere le nombre de conditional ajouté dans le commit et on l'ajoute au  nombre total de conditional
            conditional_added = conditional_added + find_occurence_in_commit(commit,"@Conditional",file)

        file.write("\n\n##### nombre de conditional dans ce projet : {}  #####".format(conditional_added))

if __name__ == '__main__' :
    #get in input.txt all the the github to explore
    f = open("input.txt", "r")
    #Set an array with all repo url
    repo_input = [line.strip() for line in f]
    #Close the file
    f.close()

    explore_commits(repo_input)


