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
	$$EMBULK_EXEC gem install embulk-input-redshift
	mkdir -p $$EMBULK_PATH/../brunch/configs

deps:
ifeq ($(OS),Darwin)
		brew install postgresql
endif
ifeq ($(OS),Linux)
		sudo apt-get install python-psycopg2
endif
		pip install -r requirements.txt

start:
	honcho -f Procfile start
