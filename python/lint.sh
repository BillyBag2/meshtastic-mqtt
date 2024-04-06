#!/bin/bash

# Search for all python files in the python directory and pylint them.
find . -name "*.py" | xargs pylint
