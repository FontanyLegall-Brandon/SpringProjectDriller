from pydriller import RepositoryMining
from util.string import remove_comments
import re
from threading import Thread

def extract_diff(repo, out_folder, regexpr):

    conditional_tag = re.compile(r'{}'.format(regexpr))

    repo = RepositoryMining(repo, only_modifications_with_file_types=['.java'])

    commits = repo.traverse_commits()

    def process(data):
        try:
            for m in data.modifications:
                code = m.diff
                code = remove_comments(code)

                matches = re.findall(conditional_tag, code)

                # Catch only commit where @conditional is in diff
                if len(matches) > 0:
                    f = open(out_folder + "/{}_commit_info.txt".format(m.hash), 'w')
                    print(m.__dict__, file=f)
                    f.close()

        except TypeError:
            # print("WARNING cannot analyse commit : ", commit.hash)
            pass

    for commit in commits:
        t = Thread(target=process, args=(commit,))
        t.start()