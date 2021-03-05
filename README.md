# cleanup-gitlab-runner

![Docker Image Version (latest semver)](https://img.shields.io/docker/v/containeroo/cleanup-gitlab-runner?style=flat-square)
![Docker Pulls](https://img.shields.io/docker/pulls/containeroo/cleanup-gitlab-runner?style=flat-square)
![Docker Image Size (tag)](https://img.shields.io/docker/image-size/containeroo/cleanup-gitlab-runner/latest?style=flat-square)
![GitHub issues](https://img.shields.io/github/issues/containeroo/cleanup-gitlab-runner?style=flat-square)
![Twitter Follow](https://img.shields.io/twitter/follow/containeroo?style=social)

## Introduction

cleanup-gitlab-runner deletes all Gitlab runners with the state `offline`.
cleanup-gitlab-runner is built to run in a CI environment (e.g. GitLab CI).

## Requirements

- GitLab

## Configration

cleanup-gitlab-runner takes the following environment variables:

| Variable        | Description                                 | Example                      |
| :-------------- | :------------------------------------------ | :--------------------------- |
| `VERIFY_SSL`    | Verify ssl certificate (defaults to `true`) | `true` or `false`            |
| `GITLAB_TOKEN`  | GitLab access token (more detail see below) | `12345678`                   |
| `CI_SERVER_URL` | GitLab URL (defaults to `CI_SERVER_URL`     | `https://gitlab.example.com` |

*GITLAB_TOKEN*
*Create the access token with an admin user*

### GitLab

If you want to use cleanup-gitlab-runner in a GitLab CI / CD job, you can use the follwing `.gitlab-ci.yml` as an example:

```yaml
image:
  name: containeroo/cleanup_gitlab_runner:latest
  entrypoint: [""]

stages:
  - cleanup_gitlab_runner

cleanup_gitlab_runner:
  stage: cleanup_gitlab_runner
  only:
    - schedules
  script: python /app/cleanup_gitlab_runner.py
```

In order to set the configration environment variables, go to your project (repository) -->  `Settings` -> `CI / CD` -> `Variabels` -> `Expand`.

After you have set all variables you can create a pipeline schedule. This ensures your job runs regularly.
