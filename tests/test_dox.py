from scripttest import TestFileEnvironment as STE
import os


DOCKER_IMAGE = os.getenv("DOCKER_IMAGE", "realcundo/dtox:test")


def run(*dtox_args, **kwargs):
    """Runs docker run with optional dtox_args. Returns ProcResult"""

    env = STE("./test-output")

    command = ["docker", "run", "--rm", "-i", DOCKER_IMAGE]
    command.extend(dtox_args)

    r = env.run(*command, **kwargs)

    # make sure it isn't a docker run failure
    if "Unable to find image" in r.stderr:
        raise ValueError(r.stderr)

    return r


def test_dtox_empty_params_no_toxini_file():

    r = run(expect_error=True)

    assert r.returncode != 0
    assert r.stdout == "using CODE_DIR=/code\n"
    assert r.stderr == "ERROR: toxini file 'tox.ini' not found\n"
    assert r.files_after == {}


def test_dtox_dot_dir_param_no_toxini_file():

    r = run(".", expect_error=True)

    assert r.returncode != 0
    assert r.stdout == ""
    assert r.stderr == "Error: Working directory must be absolute: .\n"
    assert r.files_after == {}
