# docker-tox
A docker image for running Python test suite in multiple Python versions (2.3 - 3.5, pypy) using [tox](http://tox.readthedocs.io/) without actually installing tox and all Python versions.

| OS Version | Python Versions | Docker Hub |
|------------|-----------------|------------|
| Ubuntu Trusty |Python 2.3-3.5, pypy | [![](https://images.microbadger.com/badges/version/realcundo/docker-tox.svg)](https://hub.docker.com/r/realcundo/docker-tox) [![](https://images.microbadger.com/badges/image/realcundo/docker-tox.svg)](https://hub.docker.com/r/realcundo/docker-tox) |

## Quick Start
No need to install tox or Python, just run:
```bash
docker pull realcundo/docker-tox
docker run --rm -it -v $PWD:/src:ro realcundo/docker-tox
```
This will read `tox.ini` from the local directory (`$PWD`) and run tox inside the container.

## Basic Usage
Two forms are available:
```bash
docker run --rm -it -v $PWD:/src:ro realcundo/docker-tox
```
```bash
docker run --rm -it -v $PWD:/src:ro realcundo/docker-tox tox <$WORK_DIR> [<tox-arg1>] [<tox-arg2>] [...]
```
The fomer simply runs tox inside `/code` directory.
To specify different directory and/or pass in parameters, second form must be used. *The first argument is always interpreted as a working directory.*

Tox is run as a normal user (`testuser`) and not as root.

## Use Cases
#### I want to run tox tests.
```bash
docker run --rm -it -v $PWD:/src:ro realcundo/docker-tox
```
This will copy contents of current directory to `/code` and run tox.
#### I want to run tox as if it ran from my local directory.
```bash
docker run --rm -it -v $PWD:/src:ro realcundo/docker-tox tox $PWD
```
This will create `$PWD` path inside the container and run tox. Useful if tests depend on specific path/location or when exception stacktrace file names and paths matter.
#### I want to run tox with additional parameters and I don't care where tox is run.
```bash
docker run --rm -it -v $PWD:/src:ro realcundo/docker-tox tox /code --help
```
This will create use `/code` path inside the container and pass `--help` argument to tox.

## Future Work
- ability to fetch data/artifacts from the container (probably by mapping `/code`)
- images based on other OSes (currently only Ubuntu Trusty)
- preserving `pip`/`tox` caches between runs to speed up test runs

## Links
- source code: https://github.com/realcundo/docker-tox
- docker hub: https://hub.docker.com/r/realcundo/docker-tox
