. set_environment.sh

. virtualenv/bin/activate
pytest

. virtualenv3/bin/activate
pytest

pytest --flakes
