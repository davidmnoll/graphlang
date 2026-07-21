


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

# Two TUIs side by side in tmux: left pane hosts, right pane auto-attaches.
tui-pair:
	cd rs && cargo build
	tmux kill-session -t graphlang-pair 2>/dev/null || true
	tmux new-session -d -s graphlang-pair 'rs/target/debug/graphlang'
	tmux split-window -h -t graphlang-pair 'sleep 0.3; rs/target/debug/graphlang'
	if [ -n "$$TMUX" ]; then tmux switch-client -t graphlang-pair; else tmux attach -t graphlang-pair; fi

# Two browser tabs on one session; the host TUI runs detached in tmux
# (view it with: tmux attach -t graphlang-pair).
web-pair:
	cd rs && cargo build
	tmux kill-session -t graphlang-pair 2>/dev/null || true
	tmux new-session -d -s graphlang-pair 'rs/target/debug/graphlang'
	timeout 5 sh -c 'until curl -s -o /dev/null http://localhost:7341/; do sleep 0.1; done'
	xdg-open http://localhost:7341
	sleep 0.5
	xdg-open http://localhost:7341
	@echo "host TUI is detached; view it with: tmux attach -t graphlang-pair"

# One of each: hosting TUI in tmux plus one browser tab.
tui-web:
	cd rs && cargo build
	tmux kill-session -t graphlang-pair 2>/dev/null || true
	tmux new-session -d -s graphlang-pair 'rs/target/debug/graphlang'
	timeout 5 sh -c 'until curl -s -o /dev/null http://localhost:7341/; do sleep 0.1; done'
	xdg-open http://localhost:7341
	if [ -n "$$TMUX" ]; then tmux switch-client -t graphlang-pair; else tmux attach -t graphlang-pair; fi