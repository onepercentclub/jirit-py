import re

from jira import JIRA
from github import Github


class Jirit():
    def __init__(self, jira, git):
        self.jira_id = jira['jira_id']

        try:
            self.jira = JIRA(jira['jira_url'], basic_auth=(jira['jira_username'],
                             jira['jira_passwd']))
        except KeyError as e:
            print "JIRA settings required!"
            raise e

        try:
            self.github = Github(git['git_username'], git['git_passwd'])
            self.repo = self.github.get_organization(git['git_org']).get_repo(git['git_repo'])
        except KeyError as e:
            print "GIT settings required!"
            raise e

    def tickets(self, git_from, git_to):
        c = self.repo.compare(git_from, git_to)

        tickets_ids = []
        for commit in c.commits:
            m = re.search(r'(' + self.jira_id + '-\d+)', commit.commit.message)
            if m:
                tickets_ids.append(m.group(0))

        tickets = []
        for tid in tickets_ids:
            tickets.append(self.jira.issue(tid, fields='summary,comment'))
        return tickets

    def summary(self, git_from, git_to):
        tickets = self.tickets(git_from, git_to)
        for ticket in tickets:
            print "{}: {}".format(ticket.key, ticket.fields.summary)
