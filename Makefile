build_test_env:
	docker pull trinodb/trino:391
	docker-compose -f docker-compose.yml build

start_test_env:
	docker-compose up

stop_test_env:
	docker-compose down

ifndef name
NAME=all
else
NAME=$(name)
endif

local_test:
	find . -name "*.pyc" -type f -delete
	PYTHONPATH=./src/ \
	FORMAT_NODE_ID=TRUE \
	pytest -s -vv --cov=. --testdox --cov-report term-missing $(spec) --run_name $(NAME)

test:
	docker exec -it tests_runner make local_test spec=$(spec) name=$(NAME)
