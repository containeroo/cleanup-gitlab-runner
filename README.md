# cleanup-gitlab-runner

![Docker Image Version (latest semver)](https://img.shields.io/docker/v/containeroo/cleanup-gitlab-runner?style=flat-square)
![Docker Pulls](https://img.shields.io/docker/pulls/containeroo/cleanup-gitlab-runner?style=flat-square)
![Docker Image Size (tag)](https://img.shields.io/docker/image-size/containeroo/cleanup-gitlab-runner/latest?style=flat-square)
![GitHub issues](https://img.shields.io/github/issues/containeroo/cleanup-gitlab-runner?style=flat-square)
![Twitter Follow](https://img.shields.io/twitter/follow/containeroo?style=social)

## Introduction

cleanup-gitlab-runner deletes all Gitlab runners with the state `offline`.
cleanup-gitlab-runner is built to run in a CI environment (e.g. GitLab CI) or as a Kubernetes cronjob.

## Requirements

- GitLab

## Configuration

cleanup-gitlab-runner takes the following environment variables:

| Variable                   | Description                                                                         | Example                      |
| :------------------------- | :---------------------------------------------------------------------------------- | :--------------------------- |
| `VERIFY_SSL`               | Verify ssl certificate (defaults to `true`)                                         | `true` or `false`            |
| `DRY_RUN`                  | optional, if set it will only print but not delete                                  | `true` or `false`            |
| `GITLAB_URL`               | GitLab URL (defaults to `CI_SERVER_URL`                                             | `https://gitlab.example.com` |
| `GITLAB_TOKEN`             | GitLab access token (more detail see below)                                         | `12345678`                   |
| `GITLAB_GROUP`             | optional, if set only deletes runner registered on the given group id or group name | `123` or `groupname`         |
| `GITLAB_BASEAUTH_USER`     | optional, user for additional basic authentication                                  | `my_user`                    |
| `GITLAB_BASEAUTH_PASSWORD` | optional, password for additional basic authentication                              | `my_password`                |

*GITLAB_TOKEN*
*Create the access token with an admin user*

### GitLab

If you want to use cleanup-gitlab-runner in a GitLab CI / CD job, you can use the follwing `.gitlab-ci.yml` as an example:

```yaml
image:
  name: containeroo/cleanup-gitlab-runner:latest
  entrypoint: [""]

stages:
  - cleanup-gitlab-runner

cleanup-gitlab-runner:
  stage: cleanup-gitlab-runner
  only:
    - schedules
```

In order to set the configration environment variables, go to your project (repository) -->  `Settings` -> `CI / CD` -> `Variabels` -> `Expand`.

After you have set all variables you can create a pipeline schedule. This ensures your job runs regularly.

### Kubernetes CronJob

Create a secret with a GitLab group token for a specific group or a GitLab admin token for all runners:

```yaml
---
apiVersion: v1
kind: Secret
metadata:
  name: cleanup-gitlab-runner
  namespace: gitlab
type: Opaque
stringData:
  GITLAB_TOKEN: <GITLAB_TOKEN>
```

Create a CronJob to periodically delete unused GitLab runners:

```yaml
---
apiVersion: batch/v1
kind: CronJob
metadata:
  name: cleanup-gitlab-runner
  namespace: gitlab
  labels:
    job: cleanup-gitlab-runner
spec:
  schedule: CRON_TZ=Europe/Zurich 0 4 * * *
  concurrencyPolicy: Forbid
  failedJobsHistoryLimit: 1
  successfulJobsHistoryLimit: 1
  jobTemplate:
    spec:
      template:
        metadata:
          labels:
            job: cleanup-gitlab-runner
        spec:
          restartPolicy: Never
          containers:
            - name: cleanup-gitlab-runner
              image: ghcr.io/containeroo/cleanup-gitlab-runner:latest
              env:
                - name: GITLAB_URL
                  value: http://gitlab-webservice-default.gitlab.svc.cluster.local:8080
                #- name: GITLAB_GROUP
                #  value: MY_GROUP
              envFrom:
                - secretRef:
                    name: cleanup-gitlab-runner
          automountServiceAccountToken: false

```
