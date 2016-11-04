Jirit
-----

A simple module and scripts for transitioning Jira tickets based on Github commit messages.

Usage
-----

Export environment settings for:

JIRA_EMAIL <Jira login email>
JIRA_PASSWORD <Jira login password>
JIRA_URL <Jira url, eg "https://org_name.atlassian.net" >
JIRA_ID <The Jira id added before ticket numbers, eg TT for TT-1234>
GIT_USERNAME=<Github username>
GIT_PASSWORD=<Github password>
GIT_ORG=<organization or username for the Github project, eg l33tnom for https://github.com/l33tnom/foobar>
GIT_REPO=<project name, eg foobar in the GIT_ORG example above>

Show Jira tickets based on git change
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

jirit show <commit_hash_from> <commit_hash_to>

Transition Jira tickets based on git change
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

jirit deploy <commit_hash_from> <commit_hash_to> <transition name> <match tag> <dry run>

This will trigger the <transition name> for Jira ticket if there is a git commit referenced in the git commit range, and the commit includes the tag #<match tag>. If the <dry run> flag is true then it will only display the possible transitioned issues without doing the Jira transition.

Building release
----------------

pip install twine
python setup.py sdist bdist_wheel
twine upload -s dist/jirit-1.3.5*
