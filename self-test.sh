#!/bin/bash
set -e -u

echo "Running $0 as $(id)"

# Test installed python versions

# compare python sys.version_info with expected value
check_python_version()
{
    command="$1"
    expect="$2"

    echo " - testing $command, expecting '$expect'"

    "$command" -c "import sys; assert '%s.%s' % sys.version_info[:2] == '$expect'"
}

# iterate over python versions and make sure each can be executed
for py_version in $PYTHON_VERSIONS; do
    check_python_version "python$py_version" "$py_version"
done

# pypy (reports as 2.7)
check_python_version pypy 2.7
