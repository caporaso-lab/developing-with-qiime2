.PHONY: lint install html clean cacheclean

lint:
	jupyter book build book/ \
	  --warningiserror \
	  --nitpick \
	  --keep-going \
	  --all \
	  --verbose

install:
	pip install -r requirements.txt

html:
	jupyter book build book/

clean:
	jupyter book clean book/

cacheclean:
	rm -rf book/_build/