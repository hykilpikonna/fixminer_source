#!/bin/bash
# conda activate fixminerEnv

expop PYTHONPATH=$(pwd)
export PYTHONPATH

python -u python/main.py "$@"
