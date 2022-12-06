# RUDI

Automating your home or workshop using a Raspberry Pi.......

---

## Overview

The RUDI system contains:

1. RUDI App - A python-based application that coordinates activities between physical devices based on a provided config file.

2. RUDI Admin - A web-based application that connects with one or more RUDI Apps for monitoring and confguration

---

## Running RUDI in Docker

Running RUDI in Docker insures that it will run the same way on a Pi as it does on developer machines

1. Make sure you have Docker installed 

    Tip: Docker Desktop is usually the easiest way to do this

2. Create a config.json file in the `rudi-app` folder

    Tip: You can start by copying the contents from the config-example.json file

3. From the root of the repository, run `docker compose up --build`

    Tip: You can also run this from within the `rudi-app` or `rudi-admin` folders if you want to run just one of those applications individually.

    Note: If you want to interact with the RUDI App using your keyboard (i.e. you are using a KeyboardButton device), you must run the `rudi-app` application individually like this:

         docker compose build --no-cache && docker compose run rudi-app


---

## Local Development

Waiting for a Docker image to build every time you make a small change is annoyingly slow. So here's how you can setup your local system:

### RUDI App

1. Install Python 3 (usually comes pre-installed in MacOS)

2. Install the required packages:

        pip3 install -r requirements.txt
    
    Tip: Remember to add any new packages you use to the requirements.txt file as you develope

    Note: If you are installing these dependencies anywhere other than a Pi you may have to remove the RPi.GPIO library, as it will not even install on certain systems (like Mac OS). You can just take this out of the file and then put it back after the installation.

3. Run the app:

        python3 main.py
    
    Note: Before you commit your completed work, be sure to run the Rudi App in Docker at least once to insure it will work reliably in production

### RUDI Admin

1. Instructions
2. Coming
3. Soon

---

## Logging

The logging level is set using the LOG_LEVEL environment variable.

### Levels

    - DEBUG
    - INFO
    - WARNING (this is the default)
    - ERROR
    - CRITICAL

### Docker Injection

The log level is set in the docker-compose.yml file and is injected as an environment variable

### Local Development

The easiest way set this quickly is to add to the command line before you run the app

    LOG_LEVEL=DEBUG python3 main.py

---

## Pi Deployment

### poll-build-run.py

This utility is meant to be run on a Pi when you want it to automatically run the latest code from a certain branch.

Pi Pre-Reqs:
- Internet access
- git installed
- Docker installed

Usage:
- Connect to Pi (physically or via SSH)
- Clone repo (you only have to do this step once)
- Checkout the branch you want to monitor (git checkout some-branch)
- Make sure you have a valid config file (you may also want to make sure mock pins are disabled)
- Run the utility (sh utils/poll-build-run.py)
