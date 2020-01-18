import fileinput

from pydriller import RepositoryMining, GitRepository

def find_occurence_in_commit(commit, word,file):
    conditional_added = 0
    commit_with_conditional = []
    for m in commit.modifications:
        if(format(m.source_code).find(word) != -1):
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

    for repo in repo_input :
        repofilename = "output"+ repo[repo.rfind('/'):] + ".txt"
        repofilebuffer = open(repofilename, 'w+')
        conditional_added = 0
        repofilebuffer.write("\n\n ***** le git du projet : {} *****\n".format(repo))
        for commit in RepositoryMining(repo).traverse_commits():
            conditional_added = conditional_added + find_occurence_in_commit(commit,"@Conditional",repofilebuffer)
        repofilebuffer.write("\n\n##### nombre de conditional dans ce projet : {}  #####".format(conditional_added))

if __name__ == '__main__' :
    f = open("input.txt", "r")
    repo_input = [line.strip() for line in f]
    f.close()
    explore_commits(repo_input)
