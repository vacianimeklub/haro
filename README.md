# Haro

Haro is a small Telegram bot built on the excellent [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) library, which provides a 
few functionalities that our community likes to use:

- Logging for analytics purposes to track community health based on multiple channels
- Download database so it can be analyzed with external tools (I use a Jupyter notebook with pandas for this at the moment) 
- Healthcheck endpoint (`/healthcheck`) running on port 5000
- *(in progress)* Voting 

![rolling haro](https://i.makeagif.com/media/10-21-2014/8Ivao7.gif)

### Technical details

- Tested via tox + pytest for Python 2.7, 3.7
- Uses sqlalchemy and an SQLite database (for now)
- Healthcheck is done via the Healthcheck library running on a lightweight server on port 500, built on Flask and gevent.pywsgi

### Development setup

1. Get a bot token from Botfather, as usual.
2. Check your Telegram ID with @userinfobot.
3. Clone this repo.
4. Copy the `set_environment.sh.template` file into `set_environment.sh` and fill the parameters based on step 1-2.
5. Run `setup.sh`; `tox` will set up virtualenvs for both Python versions. If you get `InterpreterNotFound` errors, it means you will need to get a Python interpreter for the given version. (On macOS, this can be solved via Homebrew; for other OSs, check https://www.python.org/downloads/ for the best option for you.)
6. Use the following commands as you see fit:
    - For starting Haro, run `./start.sh`.
    - For running unit tests, `./runtests.sh`.
    - For checking whether healthcheck works, run `./start_healthcheck.sh` and open http://localhost:5000/healthcheck in your browser.
    - If you modify the virtualenv and want to apply it to both virtualenvs, you can use the `./update_requirements.sh` command, which will try to update the virtualenvs via `tox`. For any changes where a dependency would not by updated by that (e.g. downgrading), drop the virtualenvs first with `rm -rf .tox/`.
