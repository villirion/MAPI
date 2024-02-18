run:
	python app.py

test_query:
	python query_test.py

test_persistence:
	python persistence_test.py

test:
	make test_query test_persistence