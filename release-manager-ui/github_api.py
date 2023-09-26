import json

import requests
from flask import current_app

from utils import load_json_from_file, save_json_to_file


def get_open_pull_requests():
    data = load_json_from_file("repos.json")
    if not data:
        return None

    github_data = data["github_repos"]

    pull_requests = {}

    for repo in github_data:
        owner = repo["repo_link"].split("/")[-2]
        repo_name = repo["repo_link"].split("/")[-1]

        gh_token = current_app.config["GITHUB_TOKEN"]

        url = f"https://api.github.com/repos/{owner}/{repo_name}/pulls"
        params = {
            "state": "open"
        }

        headers = {
            "Accept": "application/vnd.github.v3+json",
            "Authorization": f"Bearer {gh_token}"
        }
        response = requests.get(url, params=params, headers=headers)

        if response.status_code == 200:
            pull_requests[repo_name] = response.json()
        else:
            pull_requests[repo_name] = None

    save_json_to_file(pull_requests, "pull_requests.json")
