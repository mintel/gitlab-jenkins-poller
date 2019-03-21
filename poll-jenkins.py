#!/usr/bin/env python3
"""
Script to poll a Jenkins multibranch Git job for the latest build for a given commit.
"""

import os
# this is because our Jenkins instance uses a self signed SSL cert
os.environ["PYTHONHTTPSVERIFY"] = os.environ.get("PYTHONHTTPSVERIFY", "0")
from time import sleep
from pprint import pprint
from requests import exceptions

import jenkins


# environment variables used for parameters
jenkins_user = os.environ["JENKINS_USER"]
jenkins_password = os.environ["JENKINS_PASSWORD"]
jenkins_host = os.environ.get("JENKINS_HOST", "https://jenkins.mintel.ad")
# e.g. EVERESTUI_jobs/web
multibranch_job = os.environ["MULTIBRANCH_JOB"]
# e.g. CFD-4563
branch = os.environ["CI_COMMIT_REF_NAME"]
# full commit SHA
commit = os.environ["CI_COMMIT_SHA"]


def find_build(job, commit):
    """"
    Return the latest build for a given job and commit.

    >>> find_build("EVERESTUI_jobs/web/CFD-4563", "953e96c4ece29f64b5d23b12b0dfaa9ddb9f9f00")
    {...}
    """
    # the last 100 jobs are returned by default. depth=1 is so build objects are populated
    builds = server.get_job_info(job, depth=1)["builds"]
    for build in builds:
        build_commit = next((action["lastBuiltRevision"]["SHA1"]
                             for action in build["actions"]
                             if "lastBuiltRevision" in action),
                            None)
        if build_commit == commit:
            return build
    return None


server = jenkins.Jenkins(jenkins_host, username=jenkins_user, password=jenkins_password)
job = "%s/%s" % (multibranch_job, branch)

build = None
while True:
    try:
        build = find_build(job, commit)
    except exceptions.RequestException:
        pass
    if build:
        break
    sleep(10)

while True:
    try:
        build = server.get_build_info(job, int(build["id"]))
    except exceptions.RequestException:
        pass
    if "result" in build:
        break
    sleep(10)

result = build["result"]
print(build)
exit(0 if result == "SUCCESS" else 1)
