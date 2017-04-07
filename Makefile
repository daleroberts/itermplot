upload:
	python3 setup.py sdist register upload

clean:
	@rm -fr build dist
	@rm -fr itermplot.egg-info
	@rm -fr itermplot/__pycache__
