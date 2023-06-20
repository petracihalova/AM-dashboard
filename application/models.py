from dataclasses import dataclass, field
from typing import List

@dataclass
class JiraTicket:
    name: str
    link: str

@dataclass
class PR:
    title: str
    link: str
    link_mr: str
    merge_date: str
    merge_commit: str
    merge_order: int
    pr_author: str
    qe_status: str
    qe_note: str
    qe_author: str
    jira_tickets: List[JiraTicket]

@dataclass
class Repo:
    id: str
    name: str
    deploy_name: str = ""
    service_name: str = ""
    link: str = ""
    commit_master: str = ""
    commit_stage: str = ""
    commit_production: str = ""
    main_branch: str = ""
    release_stage_method: str = ""
    release_production_method: str = ""
    release_production_mr_url: str = ""
    date_release_production: str = ""
    days_without_release: int = 0
    release_author: str = ""
    release_committer: str = ""
    all_passed: bool = False
    list_of_pr: List[PR] = field(default_factory=list)
    list_of_pr_master_stage: List[PR] = field(default_factory=list)
    stage_build_status: bool = False
    production_build_status: bool = False
    stage_build_link: str = ""
    production_build_link: str = ""