import json

import requests
from flask import render_template, current_app

from github_api import get_open_pull_requests
from models import Repo
from utils import load_json_from_file


def overview():
    repos, error = load_json_from_file("repos.json")
    if error:
        error_msg = "The 'Overview' page should display data from 'application/data/repo.json' but the file is not found."
        return render_template("errors/404.html", error_msg=error_msg)

    return render_template("overview.html", repos=repos)

def services():
    path = current_app.config["BACKEND_API"] + "/resources"

    response = requests.get(path)
    data = response.json()

    services_list = []
    for item in data:
        if item["service_name"] == "turnpike":
            item["name"] = "turnpike-" + item["name"]

        services_list.append(Repo(**item))

    services_list = sorted(services_list, key=lambda x: x.name)

    authors = set()
    for repo in services_list:
        if not repo.list_of_pr:
            continue
        for pr in repo.list_of_pr:
            authors.add(pr["pr_author"])

    return render_template("services.html", services=services_list, authors=authors)

def open_pr():
    try:
        with open("application/data/pull_requests.json", mode="r", encoding="utf-8") as file:
            gh_pull_requests = json.load(file)
    except FileNotFoundError:
        get_open_pull_requests()
        with open("application/data/pull_requests.json", mode="r", encoding="utf-8") as file:
            gh_pull_requests = json.load(file)

    authors = set()
    for _, pr_list in gh_pull_requests.items():
        if not pr_list:
            continue
        for pr in pr_list:
            authors.add(pr["user"]["login"])

    return render_template("open_pr.html", gh_pr=gh_pull_requests, authors=authors)


def release_notes(id):
    path = current_app.config["BACKEND_API"] + "/resources/" + id

    response = requests.get(path)
    if response.status_code == 200:
        resource_data = response.json()
    else:
        resource_data = response.status_code

    additional_data = ""
    repozitory_data = load_json_from_file("repos.json")
    for _, repozitory in repozitory_data.items():
        for repo in repozitory:
            if repo["repo_link"].lower() == resource_data["link"].lower():
                additional_data = repo

    return render_template("release_notes.html", data=resource_data, additional_data=additional_data)
