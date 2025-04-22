#!/usr/bin/env bash
# exit on error
set -o errexit

echo "Starting Gunicorn server..."
gunicorn expense_splitter.wsgi:application
