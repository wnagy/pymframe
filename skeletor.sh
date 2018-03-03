#!/bin/sh

if which python >/dev/null; then
    exec python -x  ./tools/skeletor/skeletor.py
else
    echo "${0##*/}: Python not found. Please install Python." >&2
    exit 1
fi

