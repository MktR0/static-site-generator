#!/bin/bash

# Format all Python files
black .
isort . 

# Run all tests
python3 -m unittest discover -s src
