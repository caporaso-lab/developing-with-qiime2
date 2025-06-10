.PHONY: lint html clean cacheclean

lint:
	jupyter book build book/ \
	  --warningiserror \
	  --nitpick \
	  --keep-going \
	  --all \
	  --verbose

html:
	jupyter book build book/

clean:
	jupyter book clean book/

cacheclean:
	rm -rf book/_build/