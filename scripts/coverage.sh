#!/bin/bash

set -e

function run_coverage {
    local target=$1

    if [ -e "$target" ]; then
        ./$target/bin/coverage run \
            --source src/yafowil/widget/dict \
            --omit src/yafowil/widget/dict/example.py \
            -m yafowil.widget.dict.tests
        ./$target/bin/coverage report
        ./$target/bin/coverage html
    else
        echo "Target $target not found."
    fi
}

run_coverage py2
run_coverage py3
run_coverage pypy3
