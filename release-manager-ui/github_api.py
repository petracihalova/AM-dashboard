import requests
import re
from flask import current_app, render_template, abort

from utils import load_json_from_file, save_json_to_file, file_exists
import config


def get_github_repos_links(json_data):
    pattern = r"^(https?://)?(www\.)?github\.com/[\w-]+/[\w-]+/?$"
    gh_links = set()
    for category in json_data["categories"]:
        for repo in category["category_repos"]:
            for link in repo["links"]:
                if re.match(pattern, link["link_value"]):
                    gh_links.add(link["link_value"])

    return sorted(list(gh_links), key=lambda x: x.split("/")[-1])


def get_open_pull_requests():
    if not file_exists(config.SERVICES_LINKS):
        current_app.logger.warning(f"File '{config.SERVICES_LINKS}' doesn't exist.")
        abort(500)

    json_data = load_json_from_file(config.SERVICES_LINKS)
    if not json_data:
        current_app.logger.warning(f"No data found in the '{config.SERVICES_LINKS}'")
        abort(500)

    github_links = get_github_repos_links(json_data)

    pull_requests = {}
    pattern = r"(?:https?://)?(?:www\.)?github\.com/([\w-]+)/([\w-]+)/?"

    for url in github_links:
        match = re.search(pattern, url)
        if match:
            owner = match.group(1)
            repo_name = match.group(2)

        gh_token = config.GITHUB_TOKEN

        url = f"https://api.github.com/repos/{owner}/{repo_name}/pulls"
        params = {"state": "open"}

        headers = {
            "Accept": "application/vnd.github.v3+json",
            "Authorization": f"Bearer {gh_token}",
        }

        try:
            current_app.logger.info(f"Request to GitHub API, url: {url}")
            response = requests.get(url, params=params, headers=headers)

            current_app.logger.info(
                f"Response from GitHub API, status code: {response.status_code}"
            )

            if response.status_code == 200:
                json_data = response.json()
                if not json_data:
                    pull_requests[repo_name] = []
                else:
                    open_pr_list = []
                    for pr in json_data:
                        open_pr_list.append(
                            {
                                "number": pr["number"],
                                "draft": pr["draft"],
                                "title": pr["title"],
                                "created_at": pr["created_at"],
                                "user_login": pr["user"]["login"],
                                "html_url": pr["html_url"],
                            }
                        )

                    pull_requests[repo_name] = open_pr_list

            elif response.status_code == 401:
                current_app.logger.error("401 Unauthorized - check the GitHub token.")
                abort(401)

            response.raise_for_status()

        except requests.exceptions.RequestException as err:
            current_app.logger.error(f"Request Exception: {err}")
            abort(500)

        except Exception as err:
            current_app.logger.error(f"An error occurred: {err}")
            abort(500)

    save_json_to_file(pull_requests, config.PULL_REQUEST_LIST)
