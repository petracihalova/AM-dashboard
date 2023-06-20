from flask import render_template
import requests
from models import Repo
import os
import json

from utils import load_json_from_file
from github_api import get_open_pull_requests


def overview():
    data = load_json_from_file("repos.json")
    github_data = data["github_repos"]
    gitlab_data = data["gitlab_repos"]

    return render_template("overview.html", index=True, github_data=github_data, gitlab_data=gitlab_data)


def services():

    backend_api = os.environ.get("BE_API")
    path = backend_api + "/resources"

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

    return render_template("services.html", index=True, services=services_list, authors=authors)

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

    return render_template("open_pr.html", index=True, gh_pr=gh_pull_requests, authors=authors)

def release_notes(id):

    backend_api = os.environ.get("BE_API")
    path = backend_api + "/resources/" + id
    print(path)

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

    return render_template("release_notes.html", index=True, data=resource_data, additional_data=additional_data)
