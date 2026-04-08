build: *.blp main.py
	bash -c 'for BLUEPRINT_FILE in *.blp; do  blueprint-compiler.py compile $$BLUEPRINT_FILE > $${BLUEPRINT_FILE/blp/ui}; done'
	uv run main.py
compile: *.blp *.pug main.py
	bash -c 'for BLUEPRINT_FILE in *.blp; do  blueprint-compiler.py compile $$BLUEPRINT_FILE > $${BLUEPRINT_FILE/blp/ui}; done'
	bash -c 'for PUG_FILE in *.pug; do pypugjs $$PUG_FILE > $${PUG_FILE/pug/xml}; done'
	bash -c 'for XML_FILE in *.xml; do glib-compile-resources --sourcedir=. --target=gresources.gresource gresources.xml; done'
	uv run main.py
run: main.py
	uv run main.py
