.PHONY: compile devel prod perf

clean:
	rm -rf *.lua

compile: clean 
	moonc *.moon
	moonc views/*.moon

devel: compile
	lapis server development

prod: compile
	lapis server production

perf:
	httperf --server 127.0.0.1 --port 8080 --rate 3000 \
			--num-conn 3000 --num-call 10 --timeout 5 \
			--uri '/'
