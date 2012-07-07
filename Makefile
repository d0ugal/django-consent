test:
	coverage run --branch --source=consent ./setup.py test
	coverage report