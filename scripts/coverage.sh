#!/bin/sh

set -e

./bin/coverage run \
    --source src/yafowil/widget/dict \
    --omit src/yafowil/widget/dict/example.py \
    -m yafowil.widget.dict.tests
./bin/coverage report
./bin/coverage html
