.PHONY: debug
debug:
	@[ -f build/debug/Makefile ] && echo "Not calling cmake. Makefile exists." || mkdir -p build/debug;cmake -DCMAKE_BUILD_TYPE=Debug -B./build/debug -H.
	@make -C build/debug --no-print-directory

.PHONY: release
release:
	@[ -f build/release/Makefile ] && echo "Not calling cmake. Makefile exists." || mkdir -p build/release;cmake -DCMAKE_BUILD_TYPE=Release -B./build/release -H.
	@make -C build/release --no-print-directory

.PHONY: all
all: debug release

.PHONY: clean
clean:
	@rm -f `find . -print0 | grep -izZ '\./include/.*_jversion.hpp'`
	@rm -rf build
	@rm -rf lib

.PHONY: reset
reset:
	@rm -f .version

.PHONY: new
new: clean all
