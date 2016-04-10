#!/bin/bash

remote="$(git status -sb | sed -nr 's;^## [A-Za-z0-9]+\.\.\.([A-Za-z0-9]+)/.*;\1;p')"

