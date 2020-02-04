from pydriller import RepositoryMining
from util.string import remove_comments
import re
from threading import Thread

def fetch_keyword_introduce(repo, keyword):

    conditional_tag = re.compile(r'\+@Conditional.*\(')

    conds = dict()

    repo = RepositoryMining(repo, only_modifications_with_file_types=['.java'])

    commits = repo.traverse_commits()

    search = keyword


    def process(data):
        try:
            for m in data.modifications:
                matches = re.findall(conditional_tag, m.diff)
                for e in matches:
                    print(e[2:len(e)-1], data.committer_date, sep=" ; ")

        except TypeError:
            # print("WARNING cannot analyse commit : ", commit.hash)
            pass

    for commit in commits:
        t = Thread(target=process, args=(commit,))
        t.start()