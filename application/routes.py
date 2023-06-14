from flask import render_template
import requests
from models import Repo


def overview():
    return render_template("overview.html", index=True)


def repos():
    response = requests.get("http://localhost:3001/api/repositories")
    data = response.json()
    
    repos_list = []
    for item in data:
        repos_list.append(Repo(**item))

    return render_template("repos.html", index=True)


def open_pr():
    return render_template("open_pr.html", index=True)
