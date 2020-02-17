from git import Repo
from threading import Thread
import sys


def clone(repository, output_dir):
    repo = repository.strip()
    repo_name = repo.split('/')[-1].replace('.git', '')
    Repo.clone_from(repo, "{}/{}".format(output_dir, repo_name))
    print('.', end='')

if __name__ == "__main__":

    if len(sys.argv) <= 1:
        print("MISSING REPOSITORY OUTPUT DIR")
        sys.exit(1)

    else:
        output_dir = sys.argv[1]

    with open("project_url/repos_url.txt", 'r') as repos:
        repo_url_list = [e.strip() for e in repos.readlines()]

    for repo_url in repo_url_list:
        t = Thread(target=clone, args=(repo_url, output_dir,))
        t.start()
    sys.exit(0)