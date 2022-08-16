# rudi
A Raspberry Pi / Python based shop manager that mostly manages how tools and gates interact with a dust collector

---

## Building and running RUDI

RUDI uses Docker to insure that it will run the same on a Pi as on developer machines

1. Make sure you have Docker installed and Docker-Compose installed

2. Create a config.json file in the `rudi-app` folder (see example)

3. Run the system: `docker compose up --build`


---

## Dev Setup (Mac)

New approach coming soon

## Logging

### Levels

    - DEBUG
    - INFO
    - WARNING (this is the default)
    - ERROR
    - CRITICAL

The logging level is set using the LOG_LEVEL environment variable.

The easiest way set this quickly is to add to the command line:

    LOG_LEVEL=DEBUG ./dev.sh
