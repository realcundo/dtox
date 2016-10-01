#!/bin/bash
set -e

# default docker mount points
declare CODE_DIR="/code"
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

    # finally, create the leaf directory
    mkdir "$work_dir"
}



# if parameters were passed, first one is the working directory
# rest is passed in to the original tox
if [ "$#" -gt 0 ]; then
    # remove trailing slash
    CODE_DIR="${1%/}"

    # can't use . as work dir
    if [[ "$CODE_DIR" != /* ]]; then
        echo "Error: Working directory must be absolute: $1" >&2
        exit 1
    fi

    create_work_dir "$CODE_DIR"
    shift
fi

echo "using CODE_DIR=$CODE_DIR"

# copy source code to current CODE_DIR
rsync -a "$SRC_DIR/" "$CODE_DIR/"

# make $USER the owner of all code files
chown -R "$USERID":"$USERID" "$CODE_DIR"

# make sure $CODE_DIR is accessible by all (rx)
dir="$CODE_DIR"
while [[ "$dir" != "/" ]];
do
    chmod +rx "$dir"
    dir=$(dirname "$dir")
done


# run tox from $CODE_DIR, using testuser
cd "$CODE_DIR"
gosu "$USERID" python -m tox "$@"
