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

    def issues(self, git_from, git_to, match_tag=None):
        c = self.repo.compare(git_from, git_to)
        issues_ids = []

        def append(id):
            issues_ids.append(id)

        for commit in c.commits:
            message = commit.commit.message
            m = re.search(r'(' + self.jira_id + '-\d+)', message)
            if m:
                if match_tag:
                    tags = re.findall(r'(\B#\w*[a-zA-Z]+\w*)', message)
                    if "#{}".format(match_tag) in tags:
                        append(m.group(0))
                else:
                    append(m.group(0))

        issues = []
        for tid in issues_ids:
            issues.append(self.jira.issue(tid, fields='summary,comment'))
        return issues

    def transition_issues(self, git_from, git_to, transition, match_tag):
        for issue in self.issues(git_from, git_to, match_tag):
            self.jira.transition_issue(issue, transition)
            print "Resolved: {}".format(issue.fields.summary)

    def summary(self, git_from, git_to, format='html'):
        issues = self.issues(git_from, git_to)
        str = "<p>{}: {}</p>" if format == 'html' else "{}: {}"
        for issue in issues:
            print str.format(issue.key, issue.fields.summary)
