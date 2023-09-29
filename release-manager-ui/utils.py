import json
from flask import current_app

from models import Repo, PR, JiraTicket


DEFAULT_PATH = "release-manager-ui/data/"


def load_json_from_file(filename):
    try:
        with open(DEFAULT_PATH + filename, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        current_app.logger.error(f"File '{DEFAULT_PATH + filename}' not found.")
    except json.JSONDecodeError as e:
        current_app.logger.error(
            f"Error decoding JSON from file '{DEFAULT_PATH + filename}': {e}"
        )


def save_json_to_file(data, filename):
    with open(DEFAULT_PATH + filename, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)
    current_app.logger.info(f"JSON data saved to '{DEFAULT_PATH + filename}'")


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
