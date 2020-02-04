import argparse
parser = argparse.ArgumentParser()
#parser.name = "rimer.sh"
parser.add_argument("--repo", help="Github repository to analyse",
                    type=str, required=True)
parser.add_argument("--search", help="Keyword to search", type=str, required=True)


def getArgs():
    return parser.parse_args()