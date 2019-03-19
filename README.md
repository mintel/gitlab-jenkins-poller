### GitLab → Jenkins multibranch poller
This repository provides a Docker image and example `.gitlab-ci.yml` job which aims to allow teams which have their testing in Jenkins but workflow in GitLab to get the two working together loosely. It will let these teams see a build pass/fail from GitLab merge requests and commits.

This expects that you have a Git multibranch pipeline running in Jenkins and want to have a GitLab CI pipeline that polls for the creation and completion of a build for a commit.

## Use
See the `.gitlab-ci.yml.example` for what you need to add to your `.gitlab-ci.yml`. There are also secrets and environment variables you can set:

 * `JENKINS_USER` (secret) - read-only user name
 * `JENKINS_PASSWORD` (secret) - read-only user's password/API key
 * `JENKINS_HOST` (optional) - defaults to `https://jenkins.mintel.ad`
 * `MULTIBRANCH_JOB` - path that Jenkins job for the target repository, e.g. `EVERESTUI_jobs/web`
 * `PYTHONHTTPSVERIFY` (optional) - defaults to `0` so no SSL verification occurs so self-signed certificates can be used

The job then uses the provided variables (including ones GitLab injects) to find which particular job is for this branch (e.g. `EVERESTUI_jobs/web/CFD-4563`) and it then polls the job looking for the latest build for the current commit. Once that is found, it polls the build until it has a result where it will exit with 0 if successful, or 1 otherwise.

This has no timeouts, so relies on the GitLab project's timeout settings which will terminate the pipeline if it takes too long.

## Possible future work
The image is hundreds of megabytes, it could be stripped down to a few megabytes by using go and [distroless](https://github.com/GoogleContainerTools/distroless) to reduce download+cache cost.
