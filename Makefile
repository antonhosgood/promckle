.PHONY: setup
setup: build clean

build:
	mkdir -p prometheus-tsdb-dump && \
	curl -L https://github.com/ryotarai/prometheus-tsdb-dump/archive/master.tar.gz | \
	tar --strip-components=1 -xz -C prometheus-tsdb-dump && \
	cd prometheus-tsdb-dump && \
	go build -o ../bin/prometheus-tsdb-dump .

clean:
	rm -rf ./prometheus-tsdb-dump
