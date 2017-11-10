#!/bin/sh

set -e
set -u

LOCKDIR="/tmp/website-update.$(id -u)"
SITEDIR=~/website
PRODUCTION_BRANCH=master
DB_FILE=~/Database/conservancy-website.sqlite3
DB_SCRIPT=~bkuhn/django-supporters-list.sql

git_rev_name() {
    git rev-parse --abbrev-ref --symbolic-full-name "$@"
}

if ! mkdir "$LOCKDIR"; then
    test -d "$LOCKDIR"
    exit $?
fi
trap 'rmdir "$LOCKDIR"' 0 INT TERM QUIT

exitcode=0
if [ "$DB_SCRIPT" -nt "$DB_FILE" ]; then
    sqlite3 -bail -cmd ".timeout 30000" "$DB_FILE" <"$DB_SCRIPT" || exitcode=$?
fi

# If the checkout is not on the production branch,
# assume maintenance is happening and stop.
cd "$SITEDIR"
if [ "$(git_rev_name HEAD)" != "$PRODUCTION_BRANCH" ]; then
    exit "$exitcode"
fi

# Abort if the production branch isn't tracking a remote branch.
if ! git_upstream="$(git_rev_name '@{upstream}' 2>/dev/null)"; then
    exit 3
fi

IFS=/ read git_remote git_refspec <<EOF
$git_upstream
EOF
git fetch --quiet --no-tags "$git_remote" "$git_refspec"
if [ "$(git rev-parse "$PRODUCTION_BRANCH")" = "$(git rev-parse "$git_upstream")" ]; then
    exit "$exitcode"
fi

git merge --quiet --ff-only "$git_remote" "$git_refspec"
python2 -m compileall -q -x - www || exitcode=$?
chgrp -R www-data www || exitcode=$?
chmod -R g+rX-w,o+X-w www || exitcode=$?
chmod -R o+r www/conservancy/static || exitcode=$?
exit "$exitcode"
