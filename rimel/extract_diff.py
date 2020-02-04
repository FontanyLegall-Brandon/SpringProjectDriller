from pydriller import RepositoryMining
from util.string import remove_comments
import re
from threading import Thread

def fetch_keyword_introduce(repo):

    conditional_tag = re.compile(r'\+@Conditional.*\(')

    repo = RepositoryMining(repo, only_modifications_with_file_types=['.java'])

    commits = repo.traverse_commits()

    def process(data):
        try:
            for m in data.modifications:
                code = m.diff
                code = remove_comments(code)

                matches = re.findall(conditional_tag, code)
                if len(matches) > 0:
                    for e in matches:
                        print(e[2:len(e)-1], data.committer_date, sep=" ; ")

        except TypeError:
            # print("WARNING cannot analyse commit : ", commit.hash)
            pass

    for commit in commits:
        t = Thread(target=process, args=(commit,))
        t.start()