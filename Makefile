


clean: 
	rm -rf build


clean-build: 
	rm -rf build
	make build

build: 
	mkdir -p build
	cd build && cmake ..
	cd build && cmake --build . 