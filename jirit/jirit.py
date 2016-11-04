import re

from jira import JIRA
from jira.exceptions import JIRAError
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
        for tid in set(sorted(issues_ids)):
            try:
                issues.append(self.jira.issue(tid, fields='summary,comment'))
            except JIRAError:
                pass
        return issues

    def transition_issues(self, git_from, git_to, transition, match_tag, dry_run=True,
                          format='html', comment=None):
        success = []
        failure = []
        for issue in self.issues(git_from, git_to, match_tag):
            message = {
                'key': issue.key,
                'message': issue.fields.summary.replace('\'', '"')
            }

            try:
                if not dry_run:
                    self.jira.transition_issue(issue, transition, comment=comment)
                success.append(message)
            except JIRAError:
                failure.append(message)

        success_count = len(success)
        failure_count = len(failure)

        str_temp = '<p>{}{}{}</p>' if format == 'html' else '{}{}{}'
        if success_count or failure_count:
            if success_count:
                print str_temp.format(success_count, ' issues(s) transitioned:', '')
                for s in success:
                    print str_temp.format(s['key'], ': ', s['message'].encode('utf-8'))

            if failure_count:
                print str_temp.format(failure_count, ' issues(s) failed transition:', '')
                for f in failure:
                    print str_temp.format(f['key'], ': ', f['message'].encode('utf-8'))

        else:
            print str_temp.format('No tickets to transition', '', '')

    def summary(self, git_from, git_to, format='html'):
        issues = self.issues(git_from, git_to)

        str_temp = '<p>{}: {}</p>' if format == 'html' else '{}: {}'
        for issue in issues:
            print str_temp.format(issue.key, issue.fields.summary.replace('\'', '"'))
