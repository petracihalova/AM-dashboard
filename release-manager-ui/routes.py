import json

import requests
from flask import render_template, current_app

from github_api import get_open_pull_requests
from utils import load_json_from_file, create_deployments, get_pr_authors_from_deployments, file_exists


def overview():
    repos = load_json_from_file("repos.json")
    if not repos:
        error_msg = "No data to display."
        return render_template("errors/404.html", error_msg=error_msg)

    return render_template("overview.html", repos=repos)


def deployments():
    url = current_app.config["BACKEND_API"] + "/resources"

    request_exceptions = (
        requests.exceptions.HTTPError,
        requests.exceptions.ReadTimeout,
        requests.exceptions.ConnectionError,
    )

    try:
        response = requests.get(url, timeout=1)
        response.raise_for_status()

    except request_exceptions as err:
        err_message = f"{type(err).__name__}: {err}"
        current_app.logger.error(err_message)
        return render_template("errors/error.html", error_msg=err_message)

    deployments_list = create_deployments(response.json())

    authors = set()
    for repo in deployments_list:
        authors.update(get_pr_authors_from_deployments(repo.list_of_pr))
        authors.update(get_pr_authors_from_deployments(repo.list_of_pr_master_stage))

    return render_template(
        "deployments.html", deployments=deployments_list, authors=authors
    )


def open_pr():
    if not file_exists("pull_requests.json"):
        get_open_pull_requests()
    
    open_pr_list = load_json_from_file("pull_requests.json")
    if not open_pr_list:
        return render_template("errors/error.html", error_msg="")

    authors = set()
    for _, pr_list in open_pr_list.items():
        if not pr_list:
            continue
        for pr in pr_list:
            authors.add(pr["user"]["login"])

    return render_template("open_pr.html", gh_pr=open_pr_list, authors=authors)


def release_notes(id):
    path = current_app.config["BACKEND_API"] + "/resources/" + id

    response = requests.get(path)
    if response.status_code == 200:
        resource_data = response.json()
    else:
        resource_data = None

    additional_data = ""

    repozitory_data = load_json_from_file("repos.json")
    if not repozitory_data:
        error_msg = "No data to display."
        return render_template("errors/404.html", error_msg=error_msg)

    for repozitory in repozitory_data.values():
        for repo in repozitory:
            if repo["repo_link"].lower() == resource_data["link"].lower():
                additional_data = repo

    return render_template(
        "release_notes.html", data=resource_data, additional_data=additional_data
    )
