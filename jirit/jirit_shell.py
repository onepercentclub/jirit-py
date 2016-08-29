#!/usr/bin/env python

import sys
import os

from jirit import Jirit

args = sys.argv


def get_jirit():
    jira = {
        'jira_username': os.environ['JIRA_EMAIL'],
        'jira_passwd': os.environ['JIRA_PASSWORD'],
        'jira_url': os.environ['JIRA_URL'],
        'jira_id': os.environ['JIRA_ID'],
    }

    git = {
        'git_username': os.environ['GIT_USERNAME'],
        'git_passwd': os.environ['GIT_PASSWORD'],
        'git_org': os.environ['GIT_ORG'],
        'git_repo': os.environ['GIT_REPO']
    }

    return Jirit(jira, git)


def show():
    try:
        git_from = args[2]
        git_to = args[3]
    except IndexError:
        print "Git commits required!"
        sys.exit()

    get_jirit().summary(git_from, git_to)


def deploy():
    try:
        git_from = args[2]
        git_to = args[3]
        transition = args[4]
        match_tag = args[5]
        dry_run = False if args[6] in ["False", "false", "no"] else True
    except IndexError:
        print "Git commits and env required!"
        sys.exit()

    get_jirit().transition_issues(git_from, git_to, transition=transition,
                                  match_tag=match_tag, dry_run=dry_run,
                                  comment='Moved automatically by jirit.')


def main():
    if args[1] == 'deploy':
        cmd = deploy()
    else:
        cmd = show()

    return cmd

if __name__ == '__main__':
    cmd = main()
    exit(cmd)
