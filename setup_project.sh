#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r server/requirements.txt
# Restore the course dataset before starting your demonstration:
python scripts/import_ibm_data.py
cd server
python manage.py makemigrations djangoapp
python manage.py migrate
python manage.py shell < ../scripts/seed_car_models.py
printf '\nCreate a real root administrator account using: python manage.py createsuperuser\n'
printf 'Start APIs and Django in separate terminals (see README).\n'
