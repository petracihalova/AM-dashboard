import json


def load_json_from_file(file):
    with open(f"release-manager-ui/data/{file}", mode="r", encoding="utf8") as f:
        return json.load(f)


def remove_pr_drafts(gh_pull_requests):
    services_pr_without_drafts = {}
    for service, pr_list in gh_pull_requests.items():
        if not pr_list:
            services_pr_without_drafts[service] = []
            continue
        
        pr_list_without_drafts = []
        for pr in pr_list:
            if "[WIP]" in pr["title"] or pr["title"].startswith("WIP"):
                continue
            if pr["draft"]:
                continue
            pr_list_without_drafts.append(pr)

        services_pr_without_drafts[service] = pr_list_without_drafts
    return services_pr_without_drafts
