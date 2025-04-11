


clean: 
	rm -rf build


clean-build: 
	rm -rf build
	make build

build: 
	mkdir -p build
	cd build && cmake ..
	cd build && cmake --build .

build-debug: 
	make clean
	mkdir -p build
	cd build && cmake -DCMAKE_BUILD_TYPE=Debug ..
	cd build && cmake --build .

test:
	cd build && ctest -j$(nproc) --output-on-failure

clean-build-test:
	make clean-build
	make test

test-py:
	python3 -m unittest discover -s py -p "*.py" -v