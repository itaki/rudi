# rudi
A Raspberry Pi / Python based shop manager that mostly manages how tools and gates interact with a dust collector

---

## Building and running RUDI

RUDI uses Docker to insure that it will run the same on a Pi as on developer machines

1. Make sure you have Docker installed and Docker-Compose installed

2. Create a config.json file (see example) and save in the project root

3. To build the image: `docker build -t rudi-app .`

4. To run the image: `docker run -it --rm --name rudi-app-container rudi-app`

---

## Dev Setup (Mac)

This will let the app constantly reload while you develop, saving you endless keystrokes!

### Initial Setup

#### Make sure you have Homebrew installed:

    brew -v

If not, get it from (https://brew.sh/)

    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"

#### Install entr:

    brew install entr

### When you wanna do some dev:

#### Run:
    
    ./dev.sh

Pro Tip: Run this from the terminal window inside VS Code

Note: This refresh only triggers for files inside the "rudi" folder and will not notice newly created files.

If you get a permission error you may need to run:

    chmod u+x dev.sh

---

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
