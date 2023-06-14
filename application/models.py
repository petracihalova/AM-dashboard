from dataclasses import dataclass, field

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
    jira_tickets: JiraTicket

@dataclass
class Repo:
    id: str
    name: str
    link: str
    commit_master: str = ""
    commit_stage: str = ""
    commit_production: str = ""
    release_stage_method: str = ""
    release_production_method: str = ""
    date_release_production: str = ""
    days_without_release: int = 0
    list_of_pr: PR = field(default_factory=list)