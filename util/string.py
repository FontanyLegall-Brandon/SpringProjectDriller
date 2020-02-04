import re

def remove_comments(java_class):
    comments_regex = re.compile(r"//.*")
    multi_line_comments = re.compile(r"""((['"])(?:(?!\2|\\).|\\.)*\2)|\/\/[^\n]*|\/\*(?:[^*]|\*(?!\/))*\*\/""")

    java_class = re.sub(multi_line_comments,'',  java_class)
    return re.sub(comments_regex,'', java_class)