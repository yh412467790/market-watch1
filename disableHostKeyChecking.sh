#!/bin/bash
# note ">>". It creates a file if it does not exits.
# The file content we want is below
#
# Host *
#   StrictHostKeyChecking no
#

# any future command that fails will exit the script
set -e
mkdir -p ~/.ssh
touch ~/.ssh/config
echo -e "Host *\n\tStrictHostKeyChecking no\n\n" >> ~/.ssh/config
