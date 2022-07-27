import logging
import os
import sys
from collections import namedtuple

import urllib3
import validators

try:
    import gitlab
except Exception:
    sys.stderr.write("requirements are not satisfied! see 'requirements.txt'\n")
    sys.exit(1)

__version__ = "1.1.9"


def check_env_vars():
    gitlab_token = os.environ.get("GITLAB_TOKEN")
    if not gitlab_token:
        raise EnvironmentError("environment variable 'GITLAB_TOKEN' not set!")

    gitlab_url = os.environ.get("CI_SERVER_URL")
    if not gitlab_url:
        gitlab_url = os.environ.get("GITLAB_URL")

    if not gitlab_url:
        raise EnvironmentError("environment variable 'GITLAB_URL' not set!")

    if not validators.url(gitlab_url):
        raise EnvironmentError(f"environment variable 'GITLAB_URL' {gitlab_url} is not valid!")

    verify_ssl = os.environ.get("VERIFY_SSL", "false").lower() == "true"
    dry_run = os.environ.get("DRY_RUN", "false").lower() == "true"

    gitlab_group = os.environ.get("GITLAB_GROUP")
    gitlab_baseauth_user = os.environ.get("GITLAB_BASEAUTH_USER")
    gitlab_baseauth_password = os.environ.get("GITLAB_BASEAUTH_PASSWORD")

    Env_vars = namedtuple('Env_vars', ['verify_ssl',
                                       'gitlab_token',
                                       'gitlab_url',
                                       'dry_run',
                                       'gitlab_group',
                                       'gitlab_baseauth_user',
                                       'gitlab_baseauth_password']
    )

    return Env_vars(
        verify_ssl=verify_ssl,
        gitlab_token=gitlab_token,
        gitlab_url=gitlab_url,
        dry_run=dry_run,
        gitlab_group=gitlab_group,
        gitlab_baseauth_user=gitlab_baseauth_user,
        gitlab_baseauth_password=gitlab_baseauth_password,
    )

def main():
    try:
        env_vars = check_env_vars()
    except Exception as e:
        sys.stderr.write(f"{str(e)}\n")
        sys.exit(1)

    # disable http log output
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    urllib3.disable_warnings()

    try:
        conn = gitlab.Gitlab(url=env_vars.gitlab_url,
                             private_token=env_vars.gitlab_token,
                             ssl_verify=env_vars.verify_ssl,
                             http_username=env_vars.gitlab_baseauth_user,
                             http_password=env_vars.gitlab_baseauth_password)

    except Exception as e:
        sys.stderr.write(f"unable to connect to gitlab. {str(e)}\n")
        sys.exit(1)

    if env_vars.dry_run:
        sys.stdout.write(f"[DRY RUN] running in dry run mode\n")

    try:
        if env_vars.gitlab_group:
            runners = conn.groups.get(env_vars.gitlab_group).runners.list(all=True)
        else:
            runners = conn.runners.all(all=True)

    except Exception as e:
        sys.stderr.write(f"unable to get runners. {str(e)}\n")
        sys.exit(1)

    err = False
    for runner in runners:
        status = None if not hasattr(runner, 'status') else runner.status
        online = None if not hasattr(runner, 'online') else runner.online
        if status == 'online' or online:
            sys.stdout.write(f"skip runner {runner.description} (id: {runner.id}) because is online\n")
            continue
        try:
            if env_vars.dry_run:
                sys.stdout.write(f"[DRY RUN] delete runner {runner.description} (id: {runner.id})\n")
                continue

            if env_vars.gitlab_group:
                runner = conn.runners.get(runner.id) # group runner object has no delete method, so we need to get the runner object first

            runner.delete()
            sys.stdout.write(f"delete runner {runner.description} (id: {runner.id})\n")

        except Exception as e:
            sys.stderr.write(f"cannot delete runner {runner.description} (id: {runner.id}). {str(e)}\n")
            err = True

    sys.exit(1 if err else 0)


if __name__ == "__main__":
    main()
