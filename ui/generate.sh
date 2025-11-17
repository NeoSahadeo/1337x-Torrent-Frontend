#!/usr/bin/env bash

widget=(list_item.ui main_window.ui loading.ui)

parent_dir=$(dirname "$(dirname "$(readlink -f "$0")")")

for x in ${widget[@]}; do
	x=$(echo $x | grep -Poe "^\w+")
	pyuic6 -o $parent_dir/qtgen/$x.py $parent_dir/ui/$x.ui
done
