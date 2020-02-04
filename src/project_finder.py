import json
import requests
import os

clone_repos_urls = open("../project_url/data_from_api.txt", "w")

def get_json(url):
    response = requests.get(url)
    data = response.text
    parsed = json.loads(data)
    return parsed

def get_repo_info(json):
    for element in json :
            clone_repos_urls.write( element['clone_url']+"\n")

def delete_double():
    lines_seen = set() # holds lines already seen
    outfile = open("../project_url/repos_url.txt", "w")
    for line in open("../project_url/data_from_api.txt", "r"):
        if line not in lines_seen: # not a duplicate
            outfile.write(line)
            lines_seen.add(line)
    outfile.close()

def delete_tmp_file():
    os.remove("../project_url/data_from_api.txt")

if __name__ == '__main__' :

    #url de l'organisation spring project
    url_spring_projects_repo ="https://api.github.com/orgs/spring-projects/repos?q=language:java&sort=updated&page=1&per_page=90"
    json_spring_projects_repo = get_json(url_spring_projects_repo)
    get_repo_info(json_spring_projects_repo)
    #url avec une query contenant le mot clef spring, langage java trié par le plus d'étoile limité a 200 projet
    url_spring_with_stars_repo = "https://api.github.com/search/repositories?q=spring+language:java&sort=stars&order=desc&page=1&per_page=100"
    json_spring_with_star_repo = get_json(url_spring_with_stars_repo)
    get_repo_info(json_spring_with_star_repo['items'])
    url_spring_with_stars_repo = "https://api.github.com/search/repositories?q=spring+language:java&page=1&per_page=100"
    json_spring_with_star_repo = get_json(url_spring_with_stars_repo)
    get_repo_info(json_spring_with_star_repo['items'])
    delete_double()
    clone_repos_urls.close()
    delete_tmp_file()