import logging
import os
import sys
from collections import namedtuple

import urllib3

try:
    import gitlab
except Exception:
    sys.stderr.write("requirements are not satisfied! see 'requirements.txt'\n")
    sys.exit(1)

__version__ = "1.0.4"


def check_env_vars():
    verify_ssl = os.environ.get("VERIFY_SSL", "false").lower() == "true"
    gitlab_token = os.environ.get("GITLAB_TOKEN")
    gitlab_url = os.environ.get("CI_SERVER_URL")

    if not gitlab_token:
        raise EnvironmentError("environment variable 'GITLAB_TOKEN' not set!")

    if not gitlab_url:
        raise EnvironmentError("environment variable 'CI_SERVER_URL' not set!")

    Env_vars = namedtuple('Env_vars', ['verify_ssl',
                                       'gitlab_token',
                                       'gitlab_url',
                                       ]
    )

    return Env_vars(
        verify_ssl=verify_ssl,
        gitlab_token=gitlab_token,
        gitlab_url=gitlab_url,
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
                             ssl_verify=env_vars.verify_ssl)
    except Exception as e:
        sys.stderr.write(f"unable to connect to gitlab. {str(e)}\n")
        sys.exit(1)

    try:
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
            runner.delete()
            sys.stdout.write(f"delete runner {runner.description} (id: {runner.id})\n")
        except Exception as e:
            sys.stderr.write(f"cannot delete runner {runner.description} (id: {runner.id}). {str(e)}\n")
            err = True

    sys.exit(1 if err else 0)


if __name__ == "__main__":
    main()
