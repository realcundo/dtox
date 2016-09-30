from scripttest import TestFileEnvironment as STE
import os


TESTS_WORKDIR = os.path.abspath("tests-workdir")
DOCKER_IMAGE = os.getenv("DOCKER_IMAGE", "realcundo/dtox:test")


def run(*dtox_args, **kwargs):
    """Runs docker run with optional dtox_args. Returns ProcResult.

    kwargs:
        - tox_ini=<string>: contents of the tox.ini file to be used
    """

    env = STE(TESTS_WORKDIR)

    command = ["docker", "run", "--rm", "-i"]

    # map tests work dir into /src
    command.extend(["-v", '{}:/src:ro'.format(TESTS_WORKDIR)])

    tox_ini = kwargs.pop("tox_ini", None)
    if tox_ini is not None:
        env.writefile("tox.ini", content=tox_ini)

    command.append(DOCKER_IMAGE)
    command.extend(dtox_args)

    r = env.run(*command, **kwargs)

    # make sure it isn't a docker run failure
    if "Unable to find image" in r.stderr:
        raise ValueError(r.stderr)

    return r


class TestNoToxIni:

    def test_dtox_empty_params(self):

        r = run(expect_error=True)

        assert r.returncode != 0
        assert r.stdout == "using CODE_DIR=/code\n"
        assert r.stderr == "ERROR: toxini file 'tox.ini' not found\n"
        assert r.files_after == {}

    def test_dtox_dot_dir_param(self):

        r = run(".", expect_error=True)

        assert r.returncode != 0
        assert r.stdout == ""
        assert r.stderr == "Error: Working directory must be absolute: .\n"
        assert r.files_after == {}

    def test_dtox_code_dir_param(self):

        r = run("/code", expect_error=True)

        assert r.returncode != 0
        assert r.stdout == "using CODE_DIR=/code\n"
        assert r.stderr == "ERROR: toxini file 'tox.ini' not found\n"
        assert r.files_after == {}

    def test_dtox_other_dir_param(self):

        r = run("/this/dir/does/not/exist/yet", expect_error=True)

        assert r.returncode != 0
        assert r.stdout == "using CODE_DIR=/this/dir/does/not/exist/yet\n"
        assert r.stderr == "ERROR: toxini file 'tox.ini' not found\n"
        assert r.files_after == {}

    def test_dtox_root_dir_param(self):

        r = run("/root/dir", expect_error=True)

        assert r.returncode != 0
        assert r.stdout == "using CODE_DIR=/root/dir\n"
        assert r.stderr == "ERROR: toxini file 'tox.ini' not found\n"
        assert r.files_after == {}


class TestSimpleToxIni:

    tox_ini = """[tox]
envlist = py23,py24,py25,py26,py27,py33,py34,py35,pypy
skipsdist = True
"""

    def test_dtox_empty_params(self):

        # skip py32, there's something wrong with virtualenv+tox+py32
        r = run(tox_ini=self.tox_ini)

        assert r.returncode == 0
        assert "py23: commands succeeded" in r.stdout
        assert "py24: commands succeeded" in r.stdout
        assert "py25: commands succeeded" in r.stdout
        assert "py26: commands succeeded" in r.stdout
        assert "py27: commands succeeded" in r.stdout
        assert "py33: commands succeeded" in r.stdout
        assert "py34: commands succeeded" in r.stdout
        assert "py35: commands succeeded" in r.stdout
        assert "pypy: commands succeeded" in r.stdout
        assert r.stderr == ""

        assert r.files_after == r.files_before
        assert r.files_updated == {}
        assert r.files_deleted == {}
        assert r.files_created == {}

    def test_dtox_empty_params_py32_fails(self):

        tox_ini = """[tox]
envlist = py32
skipsdist = True
"""
        r = run(tox_ini=tox_ini,
                expect_error=True)

        assert r.returncode != 0
        assert "InvocationError:" in r.stdout

        assert r.files_after == r.files_before
        assert r.files_updated == {}
        assert r.files_deleted == {}
        assert r.files_created == {}
