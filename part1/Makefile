build:
	chmod a+x sorer

run:
	./sorer -f "test/text.txt" -print_col_type 0

docker:
	echo "Nothing to build, as we use Python. All good."

test:
	chmod a+x test/test-sorer
	./test/test-sorer

clean:
	chmod -x sorer
	rm -rf __pycache__

.PHONY: all test clean