import requests
import re
from flask import current_app, render_template

from utils import load_json_from_file, save_json_to_file, file_exists
from config import SERVICES_LINKS, PULL_REQUEST_LIST


def get_github_repos_links(json_data):
    pattern = r'^(https?://)?(www\.)?github\.com/[\w-]+/[\w-]+/?$'
    gh_links = set()
    for category in json_data["categories"]:
        for repo in category["category_repos"]:
            for link in repo["links"]:
                if re.match(pattern, link["link_value"]):
                    gh_links.add(link["link_value"])

    return sorted(list(gh_links), key=lambda x: x.split("/")[-1])


def get_open_pull_requests():
    if not file_exists(SERVICES_LINKS):
        current_app.logger.warning(f"File '{SERVICES_LINKS}' doesn't exist or doesn't contain links to GitHub/GitLab repos.")
        error_msg = "The list of repos not found. No data to display."
        return render_template("errors/404.html", error_msg=error_msg)
   
    json_data = load_json_from_file(SERVICES_LINKS)
    if not json_data:
        return render_template("errors/error.html", error_msg="")

    github_links = get_github_repos_links(json_data)

    pull_requests = {}
    pattern = r'(?:https?://)?(?:www\.)?github\.com/([\w-]+)/([\w-]+)/?'

    for url in github_links:
        match = re.search(pattern, url)
        if match:
            owner = match.group(1)
            repo_name = match.group(2)

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

    save_json_to_file(pull_requests, PULL_REQUEST_LIST)
