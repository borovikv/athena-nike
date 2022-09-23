install:
	pip install -r requirements.txt


create-trino:
	docker pull trinodb/trino:391

start-trino:
	docker-compose up

stop-trino:
	docker-compose down

clean:
	find . -name "*.pyc" -type f -delete

test:
	make clean
	PYTHONPATH=./src/ \
	pytest -s -vv --cov=. --testdox --cov-report term-missing $(spec)