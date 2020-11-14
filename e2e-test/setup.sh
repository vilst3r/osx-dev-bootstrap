#!/usr/bin/env bash

# Use this script for testing

if [ $(basename $PWD) == "e2e-test" ]; then
    cd ..
fi

if [ $(basename $PWD) != "osx-dev-bootstrap" ]; then
    echo "Cannot execute script in this directory"
    exit 1
fi

python3 src/run.py --test

# # UNCOMMENT WHEN READY FOR PRODUCTION
# # Require root user to execute
# if [ "$(whoami)" != "root" ]; then
#     echo "Please run the script as the root user"
#     exit 1
# fi

# # Install homebrew
# if test ! $(which brew); then
#     echo "Installing homebrew..."
#     /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
#     ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
#     brew install python
# fi

# # Install requirements for the script
# if test ! $(which pip3); then
#     echo "pip3 is not installed..."
#     exit 1
# else
#     pip3 install --user -r src/requirements.txt
# fi

# # Run main script that bootstraps the development environment
# python3 src/run.py