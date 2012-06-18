test:
	coverage run --branch --source=consent python setup.py test
	coverage report