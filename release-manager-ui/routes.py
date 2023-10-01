import re

import requests
from flask import render_template, current_app, request

from github_api import get_open_pull_requests
from utils import load_json_from_file, create_deployments, get_pr_authors_from_deployments, file_exists, get_links
from config import SERVICES_LINKS, SERVICES_LINKS_EXAMPLE, PULL_REQUEST_LIST


def overview():
    if file_exists(SERVICES_LINKS):
        repos = load_json_from_file(SERVICES_LINKS)
    else:
        repos = load_json_from_file(SERVICES_LINKS_EXAMPLE)
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
    reload_data = True if request.args.get("reload_data") == "true" else False

    if not file_exists(PULL_REQUEST_LIST) or reload_data:
        current_app.logger.info("Open PRs - downloading new data.")
        get_open_pull_requests()
    
    open_pr_list = load_json_from_file(PULL_REQUEST_LIST)
    if not open_pr_list:
        return render_template("errors/error.html", error_msg="")

    authors = set()
    for repo in open_pr_list.values():
        for pr in repo:
            authors.add(pr["user_login"])

    return render_template("open_pr.html", gh_pr=open_pr_list, authors=authors)


def release_notes(id):
    path = current_app.config["BACKEND_API"] + "/resources/" + id

    response = requests.get(path)
    if response.status_code == 200:
        resource_data = response.json()
    else:
        resource_data = None
                    
    links = get_links(resource_data["link"].lower())

    return render_template(
        "release_notes.html", data=resource_data, additional_data=links
    )
