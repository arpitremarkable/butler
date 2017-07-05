export EMBULK_PATH = $(HOME)/.embulk/bin
export EMBULK_EXEC = embulk
export PATH := $(EMBULK_PATH):$(PATH)
export OS = $(shell sh -c 'uname -s 2>/dev/null || echo not')
# export EMBULK_BUNDLE = ./butler/embulk/embulk_bundle

embulk:
	curl --create-dirs -o $$EMBULK_PATH/$$EMBULK_EXEC -L "https://dl.embulk.org/embulk-latest.jar"
	chmod +x $$EMBULK_PATH/$$EMBULK_EXEC
	# $$EMBULK_EXEC mkbundle $$EMBULK_BUNDLE
	$$EMBULK_EXEC gem install embulk-input-postgresql
	$$EMBULK_EXEC gem install embulk-output-command
	$$EMBULK_EXEC gem install embulk-output-redshift
	mkdir -p $$EMBULK_PATH/../brunch/configs

env:
	virtualenv .virtualenv

deps:
ifeq ($(OS),Darwin)
		brew install postgresql
endif
ifeq ($(OS),Linux)
		sudo apt-get install python-psycopg2
endif
		source .virtualenv/bin/activate
		pip install -r requirements.txt

start:
	source .virtualenv/bin/activate
	celery -A butler worker -l debug
	celery beat -A butler -l debug
