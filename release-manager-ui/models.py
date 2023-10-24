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
    merge_date: str
    merge_commit: str
    merge_order: int
    jira_tickets: List[JiraTicket]
    master_stage: bool
    pr_author: str
    qe_status: str
    qe_note: str
    qe_author: str


@dataclass
class ReleaseInterval:
    fromTarget: str
    toTarget: str 


@dataclass
class Repo:
    id: str
    name: str
    deploy_name: str
    service_name: str
    link: str
    commit_master: str
    commit_stage: str
    commit_production: str
    main_branch: str
    release_stage_method: str
    release_production_method: str
    release_production_mr_url: str
    date_release_production: str
    days_without_release: int
    release_author: str
    release_committer: str
    all_passed: bool
    list_of_pr: List[PR] = field(default_factory=list)
    list_of_pr_master_stage: List[PR] = field(default_factory=list)
    stage_build_status: bool = False
    production_build_status: bool = False
    stage_build_link: str = ""
    production_build_link: str = ""
    release_intervals: List[ReleaseInterval] = field(default_factory=list)
