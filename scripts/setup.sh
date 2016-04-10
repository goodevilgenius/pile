#!/bin/bash

remote="$(git status -sb | sed -nr 's;^## [A-Za-z0-9]+\.\.\.([A-Za-z0-9]+)/.*;\1;p')"
giturl="$(git config --get remote.${remote}.url)"

if [ -d build ]; then
	if ! git clone --branch gh-pages --single-branch "$giturl" -o github build
	then
		mkdir build
	fi 
done

pushd build

if [ "$(git rev-parse --show-toplevel)" != "$(pwd)" ]; then
	git init
	git remote add github "$giturl"
	git fetch github
	if ! git checkout gh-pages; then
		git checkout --orphan gh-pages
	fi 
fi 

popd
