test:
	coverage run --branch --source=appregister python setup.py test
	coverage report