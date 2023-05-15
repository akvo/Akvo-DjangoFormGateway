#!/usr/bin/env bash
# shellcheck disable=SC2155

set -eu
pip -q install --upgrade pip
pip -q install --cache-dir=.pip -r requirements.txt
pip check

echo "Running tests"
COVERAGE_PROCESS_START=./.coveragerc \
  coverage run --parallel-mode --concurrency=multiprocessing --rcfile=./.coveragerc \
  manage.py test --verbosity=3

echo "Coverage"
coverage combine --rcfile=./.coveragerc
coverage report -m --rcfile=./.coveragerc

if [[ -n "${COVERALLS_REPO_TOKEN:-}" ]] ; then
  coveralls
fi
