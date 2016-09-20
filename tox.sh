#!/bin/bash
set -e

# default docker mount points
declare -r CODE_DIR="/code"
declare -r SRC_DIR="/src"

declare -r USERID="testuser"


# creates work dir
create_work_dir()
{
    work_dir="$1"

    # make sure parent directory exists
    parent_dir=$(dirname "$work_dir")
    mkdir -p "$parent_dir"

    # if work dir is a symlink, remove it
    [ -L "$work_dir" ] && unlink "$work_dir"

    # if work dir is a directory, nuke it
    [ -d "$work_dir" ] && rm -rf "$work_dir"

    # finally, create the symlink and change the owner
    ln -s "$CODE_DIR" "$work_dir"
}



# if parameters were passed, first one is the working directory
# rest is passed in to the original tox
if [ "$#" -gt 0 ]; then
    # remove trailing slash
    d=${1%/}

    # can't use . as work dir
    if [[ "$d" != /* ]]; then
        echo "Error: Working directory must be absolute: $1"
        exit 1
    fi

    create_work_dir "$d"
    shift
    cd "$d"
else
    cd "$CODE_DIR"
fi

# copy source code to current CODE_DIR
# it's tempting to use --delete but code dir might contain
# artefacts from previous builds (like coverage) and they
# might be valuable for the user
rsync -a "$SRC_DIR/" "$CODE_DIR/"

# make $USER the owner of all code files
chown -R "$USERID":"$USERID" "$CODE_DIR"

# run tox from current directory, as usual, using testuser
gosu "$USERID" python -m tox "$@"
