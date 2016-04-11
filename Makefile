all: build deploy

build:
	bash _scripts/build.py

deploy: build
	git add -A _posts
	git commit -m "Build for $(date)"
	git push github gh-pages
