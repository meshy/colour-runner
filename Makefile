help:
	@echo "help    -- print this help"
	@echo "release -- release to PyPI"
release:
	python setup.py register sdist bdist_wheel upload
