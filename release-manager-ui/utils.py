import json
from flask import current_app
import os

from models import Repo, PR, JiraTicket


def load_json_from_file(file):
    try:
        with open(file, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        current_app.logger.error(f"File '{file.name}' not found.")
    except json.JSONDecodeError as e:
        current_app.logger.error(f"Error decoding JSON from file '{file.name}': {e}")


def save_json_to_file(data, file):
    with open(file, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)
    current_app.logger.info(f"JSON data saved to '{file.name}'")


def file_exists(filename):
    return os.path.exists(filename)


def create_pull_requests(pull_requests_data):
    if not pull_requests_data:
        return []
    pull_requests = []
    for pr_data in pull_requests_data:
        pull_request = PR(**pr_data)

        jira_tickets = []
        if pr_data["jira_tickets"]:
            for ticket in pr_data["jira_tickets"]:
                jira_tickets.append(JiraTicket(**ticket))

        pull_request.jira_tickets = jira_tickets
        pull_requests.append(pull_request)

    return pull_requests


def create_deployments(deployments_data):
    deployments_list = []

    for depl_data in deployments_data:
        deployment = Repo(**depl_data)

        deployment.list_of_pr = create_pull_requests(depl_data["list_of_pr"])
        deployment.list_of_pr_master_stage = create_pull_requests(
            depl_data["list_of_pr_master_stage"]
        )

        deployments_list.append(deployment)

    return sorted(deployments_list, key=lambda x: x.name)


def get_pr_authors_from_deployments(pr_list):
    authors = set()
    for pr in pr_list:
        authors.add(pr.pr_author)
    return authors
