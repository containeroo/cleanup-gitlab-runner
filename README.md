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

| Variable                   | Description                                                             | Example                      |
| :------------------------- | :---------------------------------------------------------------------- | :--------------------------- |
| `VERIFY_SSL`               | Verify ssl certificate (defaults to `true`)                             | `true` or `false`            |
| `GITLAB_TOKEN`             | GitLab access token (more detail see below)                             | `12345678`                   |
| `GITLAB_URL`               | GitLab URL (defaults to `CI_SERVER_URL`                                 | `https://gitlab.example.com` |
| `DRY_RUN`                  | optional, if set it will only print but not delete                      | `true` or `false`            |
| `GITLAB_GROUP`             | optional, if set only deletes runner registered on the given group id   | `123`                        |
| `GITLAB_BASEAUTH_USER`     | optional, user for additional basic authentification                    | `my_user`                    |
| `GITLAB_BASEAUTH_PASSWORD` | optional, password for additional basic authentification                | `my_password`                |

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
