from pydriller import RepositoryMining
from util.string import remove_comments
import re
from threading import Thread
import json

def extract_diff(repo, out_folder, regexpr):

    conditional_tag = re.compile(r'{}'.format(regexpr))

    repo = RepositoryMining(repo, only_modifications_with_file_types=['.java'])

    commits = repo.traverse_commits()

    def process(commit):
        try:
            for m in commit.modifications:
                code = m.diff
                code = remove_comments(code)

                matches = re.findall(conditional_tag, code)

                # Catch only commit where @conditional is in diff
                if len(matches) > 0:
                    print("FOUND {} in {}".format(matches, commit.hash))

                    with open(out_folder + "/{}.json".format(commit.hash), 'w') as f1 :
                        f1.write(str(json.dumps({"author_date": str(commit.author_date), "msg": str(commit.msg)})))

                    with open(out_folder + "/{}.txt".format(commit.hash), 'w') as f :
                        print(code, file=f)

        except TypeError:
            # print("WARNING cannot analyse commit : ", commit.hash)
            pass

    for commit in commits:
        t = Thread(target=process, args=(commit,))
        t.start()