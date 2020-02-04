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
                    f = open(out_folder + "/{}_commit_info.json".format(commit.hash), 'w')

                    print(json.dumps(m.__dict__,  default=lambda o: '<not serializable>'), file=f)
                    f.close()
                    f = open(out_folder + "/{}.txt".format(commit.hash), 'w')
                    print(code, file=f)
                    f.close()

        except TypeError:
            # print("WARNING cannot analyse commit : ", commit.hash)
            pass

    for commit in commits:
        t = Thread(target=process, args=(commit,))
        t.start()