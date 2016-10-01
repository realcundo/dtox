import pytest
from run_dtox import run


class TestSimpleToxIni:

    tox_ini = """[tox]
envlist = py26,py27,py33,py34,py35,pypy
skipsdist = True
"""

    def test_dtox_empty_params(self):

        # skip py32, there's something wrong with virtualenv+tox+py32
        r = run(tox_ini=self.tox_ini)

        assert r.returncode == 0
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

    def test_dtox_dot_dir_param(self):

        r = run(".", tox_ini=self.tox_ini, expect_error=True)

        assert r.returncode != 0
        assert r.stdout == ""
        assert r.stderr == "Error: Working directory must be absolute: .\n"

        assert r.files_after == r.files_before
        assert r.files_updated == {}
        assert r.files_deleted == {}
        assert r.files_created == {}

    @pytest.mark.parametrize("code_dir",
                             ["/code",
                              "/this/dir/does/not/exist/yet",
                              "/root/dir"])
    def test_dtox_abs_dir_param(self, code_dir):

        r = run(code_dir, tox_ini=self.tox_ini)

        assert r.returncode == 0
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
