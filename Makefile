# https://stackoverflow.com/questions/7507810/how-to-source-a-script-in-a-makefile
SHELL := /bin/bash

develop:
	pip install -q -U pip
	pip install -q -r requirements_dev.txt
	pre-commit install
	make precommit

install:
	pip install -q -r requirements.txt

full_install: develop install

precommit:
	git add .
	pre-commit run --all-files
	git add .

black:
	black src

isort:
	isort src

mypy:
	mypy src --ignore-missing-imports

pylint:
	pylint src --min-public-methods 0

flake:
	flake8 src --ignore=E501

check: black isort flake mypy precommit

fullcheck: check pylint

log:
	git log -n 5 --oneline

amend:
	git commit -C HEAD --amend

amend_ne:
	# https://stackoverflow.com/a/10237105/13070032
	git commit -C HEAD --amend --no-edit

git_user:
	git config --global user.name "partham16"
	git config --global user.email "43367843+partham16@users.noreply.github.com"

colab_rsa:
	# https://stackoverflow.com/a/793867/13070032
	mkdir -p /root/.ssh
	cp ../.ssh/demo_classification/* /root/.ssh/
	ssh-add /root/.ssh/id_ed25519

chmodx:
	# https://github.com/pre-commit/pre-commit/issues/413#issuecomment-248978104
	chmod +x py37/bin/pre-commit
	chmod +x .git/hooks/pre-commit
	# for black flake pylint ...
	chmod +x py37/bin/*
	ls -la py37/bin/pre-commit

colab: git_user colab_rsa chmodx

venv:
	# https://askubuntu.com/questions/1268833/error-command-path-to-env-bin-python3-7-im-ensurepip-upgrade
	sudo apt-get install python3.7-venv
	python3 -m venv py37

get_bz2:
	# https://stackoverflow.com/questions/12806122/missing-python-bz2-module/61464947#61464947
	sudo apt-get install libbz2-dev
	sudo cp /usr/lib/python3.8/lib-dynload/_bz2.cpython-38-x86_64-linux-gnu.so  /usr/local/lib/python3.8/

get_bz2_venv:
	sudo cp /usr/lib/python3.8/lib-dynload/_bz2.cpython-38-x86_64-linux-gnu.so  /workspaces/demo_classification/.venv/lib/python3.8/site-packages/
