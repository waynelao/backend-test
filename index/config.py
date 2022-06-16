"""Index development configuration."""

import pathlib

# Root of this application, useful if it doesn't occupy an entire domain
APPLICATION_ROOT = '/'

TESTING = True

INDEX_ROOT = pathlib.Path(__file__).resolve().parent.parent

# Database file is var/insta485.sqlite3
DATABASE_FILENAME = INDEX_ROOT/'var'/'netflix.sqlite3'