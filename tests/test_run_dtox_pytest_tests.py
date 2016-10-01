from run_dtox import run

# tox.ini for pytest
tox_ini = """
[tox]
envlist =  py23,py24,py25,py26,py27,py33,py34,py35,pypy
skipsdist = True

[testenv]
deps = pytest
commands = py.test
"""


# source file to be tested
source_file = """
def func(x):
    if x > 0:
        return x+1
    else:
        return x-1
"""


# pytest test
test_file = """
from source import func


def test_zero():
    assert func(0) == -1


def test_positive():
    assert func(10) == 11


def test_negative():
    assert func(-10) == -11
"""


class TestRunDtoxPytestTests:

    def write_files(self, env):
        env.writefile("source.py",
                      content=source_file)

        env.writefile("test_source.py",
                      content=test_file)

    def test_run_pytest(self):

        r = run(tox_ini=tox_ini, setup=self.write_files)

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
