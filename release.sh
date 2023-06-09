#!/bin/bash

git checkout main
git pull
git fetch --tags

LIB_NAME="Akvo-DjangoFormGateway"
CURRENT_VERSION=$(< ./src/AkvoDjangoFormGateway/__init__.py tr ' ' _ \
    | grep __version__ \
    | cut -d "=" -f2 \
    | sed 's/"//g' \
    | sed 's/_/v/g'
)
CURRENT_TAG=$(git describe --abbrev=0)

if [[ "$CURRENT_VERSION" == "$CURRENT_TAG" ]]; then
    printf "Please modify version\n"
    printf "Located at ./src/AkvoDjangoFormGateway/__init__.py\n"
    printf "Latest Release: %s %s" "$LIB_NAME" "$CURRENT_TAG"
    exit 0
fi

function push_release() {
    # GitHub CLI api
    # https://cli.github.com/manual/gh_api
    gh api \
        --method POST \
        -H "Accept: application/vnd.github+json" \
        "/repos/akvo/Akvo-DjangoFormGateway/releases" \
        -f tag_name="$1" \
        -f target_commitish='main' \
        -f name="$LIB_NAME $1" \
        -f body="$(printf "%s" "$2")" \
        -F draft=false \
        -F prerelease=false \
        -F generate_release_notes=false
}

if [[ $# -eq 0 ]]; then
    printf "Please write description\n"
    read -r DESC
    printf "Release: %s %s\n" "$LIB_NAME" "$CURRENT_VERSION"
    git tag -a "$CURRENT_VERSION" -m "New Release $CURRENT_VERSION: $DESC"
    git push --tags
    printf "%s" "${DESC}"
    push_release "${CURRENT_VERSION}" "${DESC}"
fi
