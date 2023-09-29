import os
from pathlib import Path


BACKEND_API = os.environ.get("BACKEND_API")

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
GITLAB_TOKEN = os.environ.get("GITLAB_TOKEN")

# Filenames
SERVICES_LINKS = Path("release-manager-ui/data/services_links.json")
SERVICES_LINKS_EXAMPLE = Path("release-manager-ui/data/services_links_example.json")
PULL_REQUEST_LIST = Path("release-manager-ui/data/pull_request_list.json")
