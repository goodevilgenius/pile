all: build deploy

build:
	bash scripts/build.sh

deploy: build
	git --work-tree=build --git-dir=build/.git add -A
	git --work-tree=build --git-dir=build/.git commit -m "Build for $(date)"
	git --work-tree=build --git-dir=build/.git push github gh-pages

setup:
	bash scripts/setup.sh


