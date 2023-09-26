import json

import requests
from flask import render_template, current_app

from github_api import get_open_pull_requests
from models import Repo
from utils import load_json_from_file, remove_pr_drafts


def overview():
    try:
        repos = load_json_from_file("repos.json")
    except FileNotFoundError:
        error_msg = "The 'Overview' page should display data from 'release-manager-ui/data/repos.json' but the file is not found."
        return render_template("errors/404.html", error_msg=error_msg)

    return render_template("overview.html", repos=repos)


def deployments():
    path = current_app.config["BACKEND_API"] + "/resources"

    response = requests.get(path)
    data = response.json()

    deployments_list = []
    for item in data:
        if item["service_name"] == "turnpike":
            item["name"] = "turnpike-" + item["name"]

        deployments_list.append(Repo(**item))

    deployments_list = sorted(deployments_list, key=lambda x: x.name)

    authors = set()
    for repo in deployments_list:
        if not repo.list_of_pr:
            continue
        for pr in repo.list_of_pr:
            authors.add(pr["pr_author"])

    return render_template("deployments.html", deployments=deployments_list, authors=authors)


def open_pr():
    try:
        with open(
            "release-manager-ui/data/pull_requests.json", mode="r", encoding="utf-8"
        ) as file:
            gh_pull_requests = json.load(file)
    except FileNotFoundError:
        try:
            get_open_pull_requests()
        except FileNotFoundError:
            error_msg = "The 'Open PRs' page should display data from 'release-manager-ui/data/repos.json' but the file is not found."
            return render_template("errors/404.html", error_msg=error_msg)
        with open(
            "release-manager-ui/data/pull_requests.json", mode="r", encoding="utf-8"
        ) as file:
            gh_pull_requests = json.load(file)

    authors = set()
    for _, pr_list in gh_pull_requests.items():
        if not pr_list:
            continue
        for pr in pr_list:
            authors.add(pr["user"]["login"])

    pr_list_without_drafts = remove_pr_drafts(gh_pull_requests)

    return render_template("open_pr.html", gh_pr=pr_list_without_drafts, authors=authors)


def release_notes(id):
    path = current_app.config["BACKEND_API"] + "/resources/" + id

    response = requests.get(path)
    if response.status_code == 200:
        resource_data = response.json()
    else:
        resource_data = None

    additional_data = ""
    try:
        repozitory_data = load_json_from_file("repos.json")
    except FileNotFoundError:
        error_msg = "The 'Release notes' page should display data from 'release-manager-ui/data/repos.json' but the file is not found."
        return render_template("errors/404.html", error_msg=error_msg)

    for _, repozitory in repozitory_data.items():
        for repo in repozitory:
            if repo["repo_link"].lower() == resource_data["link"].lower():
                additional_data = repo

    return render_template(
        "release_notes.html", data=resource_data, additional_data=additional_data
    )
