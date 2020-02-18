
import os
import subprocess
from pydriller import RepositoryMining
import time
repo_folder = "../../repos/"

repos = os.listdir(repo_folder)


def new_mont_value(value):
    value += 1
    value %= 13
    return 1 if value == 0 else value


for repo in repos:
    if repo != "generator-jhipster":
        continue
    repository_folder = "{}{}/".format(repo_folder, repo)
    print(repository_folder)
    repository = RepositoryMining(repository_folder, only_modifications_with_file_types=['.java'])

    selected_commits = dict()

    commits = repository.traverse_commits()

    with open("../out/{}.csv".format(repo.replace(".git", "")), 'w') as output:

        for commit in commits:
            p = subprocess.Popen('cd {}/ ; git checkout {} --quiet --force; grep -h -r -P "@Conditional.*\(" --include=*.java . | wc -l '.format(repository_folder, commit.hash), stdout=subprocess.PIPE, shell=True)

            (stdout, stderr) = p.communicate()
            p.wait()
            commit_date = commit.committer_date.date()
            str_date = '{}-{}'.format(commit_date.year, commit_date.month)
            p2 = subprocess.Popen(
                'cd {}/ ; grep -h -r -P "@Profile.*\(" --include=*.java . | wc -l '.format(
                    repository_folder, commit.hash), stdout=subprocess.PIPE, shell=True)

            (stdout2, stderr2) = p2.communicate()
            p2.wait()

            print(commit.committer_date, int(stdout.decode()), int(stdout2.decode()), sep=" ; ")
            print(commit.committer_date, int(stdout.decode()), int(stdout2.decode()), sep=" ; ", file=output)

            p = subprocess.Popen('cd {}/ ; git checkout master --force --quiet ; git reset HEAD --hard --quiet '.format(repository_folder), shell=True,
                                 stdout=subprocess.PIPE)

            p.wait()
        output.close()