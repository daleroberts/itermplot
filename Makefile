upload:
	pandoc --from=markdown --to=rst --output=README README.md
	python3 setup.py sdist
	twine upload dist/*

clean:
	@rm -fr build dist
	@rm -fr itermplot.egg-info
	@rm -fr itermplot/__pycache__
