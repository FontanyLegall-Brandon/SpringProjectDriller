
import os

from pydriller import RepositoryMining

repo_folder = "../../repos"

repos = os.listdir(repo_folder)


def new_mont_value(value):
    value += 1
    value %= 13
    return 1 if value == 0 else value


for repo in repos[:1]:

    repository = RepositoryMining("{}/{}".format(repo_folder, repo), only_modifications_with_file_types=['.java'])

    selected_commits = dict()

    for commit in repository.traverse_commits():
        commit_date = commit.committer_date.date()
        str_date = '{}-{}'.format(commit_date.year, commit_date.month)

        if str_date not in selected_commits.keys():
            selected_commits[str_date] = commit.hash
            print('{}-{}'.format(commit_date.year, commit_date.month), commit.hash)