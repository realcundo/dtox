import pytest
from run_dtox import run


class TestToxUsesCorrectPython:

    @pytest.mark.parametrize("pyenv,output",
                             [
                                 ("py23", "2, 3"),
                                 ("py24", "2, 4"),
                                 ("py25", "2, 5"),
                                 ("py26", "2, 6"),
                                 ("py27", "2, 7"),
                                 ("py33", "3, 3"),
                                 ("py34", "3, 4"),
                                 ("py35", "3, 5"),
                                 ("pypy", "2, 7"),
                             ])
    def test_run_tox(self, pyenv, output):

        expected_output = "({})\n".format(output)

        tox_ini = """[tox]
envlist = {}
skipsdist = True

[testenv]
commands = python -c "import sys; print(sys.version_info[:2])"
""".format(pyenv)

        r = run(tox_ini=tox_ini)

        assert r.returncode == 0
        assert r.stderr == ""
        assert expected_output in r.stdout, r.stdout
        assert r.files_after == r.files_before
