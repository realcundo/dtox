# dtox (docker-tox)
A docker image for running Python test suite in multiple Python versions (2.6 - 3.5, pypy) using [tox](http://tox.readthedocs.io/) without actually installing tox and all Python versions.

| OS Version | Python Versions | Travis CI |Docker Hub |
|------------|-----------------|-----------|-----------|
| Ubuntu Trusty |Python 2.6-3.5, pypy | [![Build Status](https://travis-ci.org/realcundo/dtox.svg?branch=master)](https://travis-ci.org/realcundo/dtox) | [![](https://images.microbadger.com/badges/version/realcundo/dtox.svg)](https://hub.docker.com/r/realcundo/dtox) [![](https://images.microbadger.com/badges/image/realcundo/dtox.svg)](https://hub.docker.com/r/realcundo/dtox) |

## Quick Start
No need to install tox or Python, just run:
```bash
docker pull realcundo/dtox
docker run --rm -it -v $PWD:/src:ro realcundo/dtox
```
This will read `tox.ini` from the local directory (`$PWD`) and run tox inside the container.

Handy alias to run `dtox` as a drop-in replacement of `tox`:
```bash
alias dtox='docker run --rm -it -v "$PWD":/src:ro realcundo/dtox "$PWD"'
```

## Basic Usage
Two forms are available:
```bash
docker run --rm -it -v $PWD:/src:ro realcundo/dtox
```
```bash
docker run --rm -it -v $PWD:/src:ro realcundo/dtox <$WORK_DIR> [<tox-arg1>] [<tox-arg2>] [...]
```
The fomer simply runs tox inside `/code` directory.
To specify different directory and/or pass in parameters, second form must be used. *The first argument is always interpreted as a working directory.*

Tox is run as a normal user (`testuser`) and not as root.

## Use Cases
#### I want to run tox tests.
```bash
docker run --rm -it -v $PWD:/src:ro realcundo/dtox
```
This will copy contents of current directory to `/code` and run tox.

#### I want to run tox as if it ran from my local directory.
```bash
docker run --rm -it -v $PWD:/src:ro realcundo/dtox $PWD
```
or if you have the `alias`, simply:
```bash
dtox
```
This will create `$PWD` path inside the container and run tox. Useful if tests depend on specific path/location or when exception stacktrace file names and paths matter.

#### I want to run tox with additional parameters and I don't care where tox is run.
```bash
docker run --rm -it -v $PWD:/src:ro realcundo/dtox /code --help
```
or:
```bash
dtox --help
```
This will create use `/code` or `$PWD` path inside the container and pass `--help` argument to `tox`. You can of course pass in any parameter, not just `--help`.

## Future Work
- ability to fetch data/artifacts from the container (probably by mapping `/code`)
- images based on other OSes (currently only Ubuntu Trusty)
- preserving `pip`/`tox` caches between runs to speed up test runs

## Links
- source code: https://github.com/realcundo/dtox
- docker hub: https://hub.docker.com/r/realcundo/dtox
