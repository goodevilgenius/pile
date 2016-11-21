export PATH := $(HOME)/bin:$(PATH):/usr/local/bin

POINT=$(shell echo $$((RANDOM%79+128512)) )
EMOJI=$(shell printf '%x' $(POINT) )
BRANCH=$(shell git rev-parse --abbrev-ref HEAD)

all: deploy

build:
	python _scripts/pile_driver.py

stage: build
	bundle exec jekyll build -c '_config.yml,_config.local.yml'

deploy: build
	[ $(BRANCH) = gh-pages ]
	git add -A _posts _data archives
	git commit -m "[Add] `printf "\U$(EMOJI)"` `date`: `fortune -s | tr '\n' ' ' | sed -r 's/[[:blank:]]+/ /g'`"
	git push github gh-pages
