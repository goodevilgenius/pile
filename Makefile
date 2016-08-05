export PATH := $(HOME)/bin:$(PATH):/usr/local/bin

all: deploy

build:
	python _scripts/build.py

stage: build
	bundle exec jekyll build -c '_config.yml,_config.local.yml'

deploy: build
	git add -A _posts _data archives
	git commit -m "[Add] `date`: `fortune -s | tr \\n ' ' | sed -r 's/[[:blank:]]+/ /g'`"
	git push github gh-pages
