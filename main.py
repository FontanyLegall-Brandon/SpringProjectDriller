from rimel.extract_diff import extract_diff
from rimel.fetch_keyword_introduce import fetch_keyword_introduce
from util import argparser

from pydriller import *

"""
Example usage
python3 main.py --repo https://github.com/spring-projects/spring-boot.git --search "@Conditional"
"""
if __name__ == '__main__':
    args = argparser.getArgs()

    repo = args.repo
    search = args.search
    if args.extract_diff:
        extract_diff(repo, args.out, search)

    #fetch_keyword_introduce(repo, search)