export EMBULK_PATH = ~/.embulk/bin
export EMBULK_EXEC = embulk
export PATH := $(EMBULK_PATH):$(PATH)
# export EMBULK_BUNDLE = ./butler/embulk/embulk_bundle

embulk:
	# curl --create-dirs -o $$EMBULK_PATH/$$EMBULK_EXEC -L "https://dl.embulk.org/embulk-latest.jar"
	# chmod +x $$EMBULK_PATH/$$EMBULK_EXEC
	# # $$EMBULK_EXEC mkbundle $$EMBULK_BUNDLE
	# $$EMBULK_EXEC gem install embulk-input-postgresql
	# $$EMBULK_EXEC gem install embulk-output-command
	$$EMBULK_EXEC gem install embulk-output-redshift
