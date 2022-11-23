# RUDI

Automating your home or workshop using a Raspberry Pi..

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

    Tip:  You can also run this from within the rudi-app or rudi-admin folders if you want to run those applications individually

---

## Local Development

Waiting for a Docker image to build every time you make a small change is annoyingly slow. So here's how you can setup your local system:

### Rudi App

1. Install Python 3 (usually comes pre-installed in MacOS)

2. Install the required packages:

        pip3 install -r requirements.txt

3. Run the app:

        python3 main.py

3. Make sure you add any new packages you use to the requirements.txt file

4. Before you commit your completed work, be sure to run the RUDI App in Docker at least once to insure it will work properly in the wild

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
