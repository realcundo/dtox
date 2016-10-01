import pytest
from run_dtox import run


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

    @pytest.mark.parametrize("code_dir",
                             ["/code",
                              "/this/dir/does/not/exist/yet",
                              "/root/dir"])
    def test_dtox_abs_dir_param(self, code_dir):

        r = run(code_dir, expect_error=True)

        assert r.returncode != 0
        assert r.stdout == "using CODE_DIR={}\n".format(code_dir)
        assert r.stderr == "ERROR: toxini file 'tox.ini' not found\n"
        assert r.files_after == {}
