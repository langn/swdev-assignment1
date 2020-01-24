build:
	chmod a+x sorer

run:
	chmod a+x sorer
	./sorer -f "test/text.txt" -print_col_type 0

docker:
	echo "Nothing to build, as we use Python. All good."

test:
	chmod a+x sorer
	./sorer -t

clean:
	chmod -x sorer
	rm -rf __pycache__

.PHONY: all test clean