#!/bin/bash
for i in {1..24};
do
    padded="0$i"
    formatted="${padded:(-2)}"
    target_dir="src/day$formatted"
    if [ ! -d "$target_dir" ]; then
        echo $target_dir
        mkdir $target_dir

        cp -a ./template.py "$target_dir/__init__.py"
        echo "" >> "$target_dir/__init__.py"
        echo "# Started: $(date)" >> "$target_dir/__init__.py"

        touch "$target_dir/sample.txt"
        touch "$target_dir/puzzle.txt"

        git add "$target_dir/__init__.py"

        break
    fi
done