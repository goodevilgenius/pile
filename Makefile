export PATH := $(HOME)/bin:$(PATH):/usr/local/bin

all: deploy

build:
	python _scripts/build.py
	/usr/local/bin/jekyll build -c '_config.yml,_config.local.yml'

deploy: build
	git add -A _posts _data
	git commit -m "Build for `date`"
	git push github gh-pages
