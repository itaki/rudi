# rudi
A Raspberry Pi / Python based shop manager that mostly manages how tools and gates interact with a dust collector

---

## Running Rudi

This project was built and tested using Anaconda on a Mac. The instructions below assume you are using the same!

1. Make sure you have a Python 3.9 environment setup

    `conda create --name rudi python=3.9`

2. Create a config.json file (see example) and save in the project root

3. Run `python main.py`

---

## Dev Setup (Mac)

This will let the app constantly reload while you develop, saving you endless keystrokes!

### Initial Setup

#### Make sure you have Homebrew installed:

    `brew -v`

If not, get it from (https://brew.sh/)

#### Install entr:

    `brew install entr`

### When you wanna do some dev:

#### Run:
    `./dev.sh`

Pro Tip: Run this from the terminal window inside VS Code

Note: This refresh only triggers for files inside the "rudi" folder and will not notice newly created files.

If you get a permission error you may need to run:

    `chmod u+x dev.sh`

---

## Logging

### Levels

    - DEBUG
    - INFO
    - WARNING
    - ERROR
    - CRITICAL

To change the logging level, change the "logging_level" value in the config file to one of the values above