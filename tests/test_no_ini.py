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
