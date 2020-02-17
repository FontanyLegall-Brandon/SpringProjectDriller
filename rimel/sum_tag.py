
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


for repo in repos[1:2]:
    repository_folder = "{}{}/".format(repo_folder, repo)
    repository = RepositoryMining(repository_folder, only_modifications_with_file_types=['.java'])

    selected_commits = dict()

    for commit in repository.traverse_commits():
        commit_date = commit.committer_date.date()
        str_date = '{}-{}'.format(commit_date.year, commit_date.month)

        if str_date not in selected_commits.keys():
            selected_commits[str_date] = commit.hash
            print('{}-{}'.format(commit_date.year, commit_date.month), commit.hash)


    for commit in selected_commits.keys():
        p = subprocess.Popen('cd {}/ ; git checkout {} --quiet ; grep -h -r -P "@Conditional.*\(" . | wc -l '.format(repository_folder, selected_commits[commit]), stdout=subprocess.PIPE, shell=True)

        (stderr, stdout) = p.communicate()
        p.wait()

        print(stderr, stdout, sep=" \n ")

        p = subprocess.Popen('cd {}/ ; git checkout master --force --quiet ; git reset HEAD --hard --quiet '.format(repository_folder), shell=True,
                             stdout=subprocess.PIPE)