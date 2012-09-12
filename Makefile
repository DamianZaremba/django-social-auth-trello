# https://gist.github.com/3697234
publish:
	python setup.py sdist upload

clean:
	rm -rf *.egg-info
	rm -rf dist
	rm -rf build

pep8:
	flake8 --exclude=migrations,.git \
			--ignore=E501,E225,E121,E123,E124,E125,E127,E128,W404 \
			--exit-zero django_social_auth_trello

.PHONY: publish clean
