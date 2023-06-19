import requests
import os
import json

from utils import load_json_from_file


def get_open_pull_requests():
    data = load_json_from_file("repos.json")
    github_data = data["github_repos"]

    pull_requests = {}

    for repo in github_data:
        owner = repo["repo_link"].split("/")[-2]
        repo_name = repo["repo_link"].split("/")[-1]

        GH_token = os.environ.get('GH_TOKEN')

        url = f"https://api.github.com/repos/{owner}/{repo_name}/pulls"
        params = {
            "state": "open"
        }

        headers = {
            "Accept": "application/vnd.github.v3+json",
            "Authorization": f"Bearer {GH_token}"
        }

        response = requests.get(url, params=params, headers=headers)

        if response.status_code == 200:
            pull_requests[repo_name] = response.json()
        else:
            pull_requests[repo_name] = None


    with open("application/data/pull_requests.json", mode="w", encoding="utf-8") as file:
        json.dump(pull_requests, file, indent=4)
