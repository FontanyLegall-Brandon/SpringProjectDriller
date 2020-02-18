
import os
import re
import subprocess
from threading import Thread

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

        conditional_tag = re.compile(r'\+@Conditional.*\(')
        profile_tag = re.compile(r'\+@Profile.*\(')
        conditional_remove_tag = re.compile(r'-@Conditional.*\(')
        profile_remove_tag = re.compile(r'-@Profile.*\(')
        conds = dict()

        repo = RepositoryMining(repo)

        print("DATE, +@Conditional, +@Profile, -@Conditional, -@Profile")
        print("DATE, +@Conditional, +@Profile, -@Conditional, -@Profile", file=output)
        for commit in commits:
            for m in commit.modifications:
                cond_introduce = re.findall(conditional_tag, m.diff)
                profile_introduce = re.findall(profile_tag, m.diff)

                cond_removed = re.findall(conditional_remove_tag, m.diff)
                profile_removed = re.findall(profile_remove_tag, m.diff)

                if len(cond_introduce) > 0 or len(profile_introduce) > 0 or len(cond_removed) > 0 or len(profile_removed) > 0:
                    print(commit.committer_date,
                          len(cond_introduce),
                          len(profile_introduce),
                          len(cond_removed),
                          len(profile_removed),
                          sep=',')
                    print(commit.committer_date,
                          len(cond_introduce),
                          len(profile_introduce),
                          len(cond_removed),
                          len(profile_removed),
                          sep=',', file=output)