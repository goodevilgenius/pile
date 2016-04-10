# Pile

A static site generator using [DropLogger](https://github.com/goodevilgenius/droplogger), GNU Make, and GitHub Pages

## Installation

First, you must be using
[DropLogger](https://github.com/goodevilgenius/droplogger), and have a log in it
that you want to publish as a tumblelog.

The `droplogger` script should be in your PATH. Presently, the best way is to 
symlink the script. A future version will inlude a setup.py script.

Next, fork this repo, and clone it to your local machine (the machine with
DropLogger installed).

Run `make setup`, and edit `config.json` with the appropriate values.

## Running

Run `make build` and check that the `build` directory looks right to you. Then
run `make deploy` which will deploy the push the contents of the `build`
directory to the gh-pages branch of your repo.

`make` or `make all` will run `build` and `deploy`.
